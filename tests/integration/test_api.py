"""Tests d'intégration de l'API Flask du Triangulator."""

import importlib

import pytest

from triangulator.app import app
from triangulator.binary import serialize_pointset


@pytest.fixture
def client():
    """Client Flask de test."""
    return app.test_client()


def test_get_triangulation_returns_501(client):
    """Un ID non-UUID doit être rejeté en 400."""
    response = client.get("/triangulation/testid")
    assert response.status_code == 400


def test_invalid_id_format(client):
    """Un ID invalide doit produire 400."""
    response = client.get("/triangulation/not-a-uuid")
    assert response.status_code == 400


class _FakeResponse:
    def __init__(self, status_code: int, content: bytes = b""):
        self.status_code = status_code
        self.content = content


def test_triangulation_happy_path(client, monkeypatch):
    """Retourne 200 + binaire si le PointSetManager renvoie un PointSet valide."""

    def fake_get(url, timeout):
        assert "/pointset/" in url
        assert timeout == 2
        points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
        return _FakeResponse(200, serialize_pointset(points))

    app_module = importlib.import_module("triangulator.app")
    monkeypatch.setattr(app_module.requests, "get", fake_get)

    response = client.get("/triangulation/123e4567-e89b-12d3-a456-426614174000")
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/octet-stream")
    assert len(response.data) >= 8  # N + au moins un point


def test_triangulation_pointset_not_found(client, monkeypatch):
    """Retourne 404 si le PointSetManager indique que l'ID n'existe pas."""

    def fake_get(url, timeout):
        return _FakeResponse(404, b"")

    app_module = importlib.import_module("triangulator.app")
    monkeypatch.setattr(app_module.requests, "get", fake_get)
    response = client.get("/triangulation/123e4567-e89b-12d3-a456-426614174000")
    assert response.status_code == 404


def test_triangulation_pointset_manager_unavailable(client, monkeypatch):
    """Retourne 503 si le PointSetManager est injoignable."""
    import requests

    def fake_get(url, timeout):
        raise requests.RequestException("boom")

    app_module = importlib.import_module("triangulator.app")
    monkeypatch.setattr(app_module.requests, "get", fake_get)
    response = client.get("/triangulation/123e4567-e89b-12d3-a456-426614174000")
    assert response.status_code == 503


def test_api_400_when_pointset_manager_returns_400(client, monkeypatch):
    """Le Triangulator doit propager une 400 (requête invalide côté PSM)."""

    def fake_get(*_args, **_kwargs):
        return _FakeResponse(400)

    app_module = importlib.import_module("triangulator.app")
    monkeypatch.setattr(app_module.requests, "get", fake_get)

    resp = client.get("/triangulation/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 400
    assert resp.get_json()["code"] == "BAD_REQUEST"


def test_api_503_when_pointset_manager_returns_unexpected_status(client, monkeypatch):
    """Une réponse inattendue du PSM doit donner une erreur 503 dédiée."""

    def fake_get(*_args, **_kwargs):
        return _FakeResponse(418)

    app_module = importlib.import_module("triangulator.app")
    monkeypatch.setattr(app_module.requests, "get", fake_get)

    resp = client.get("/triangulation/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 503
    assert resp.get_json()["code"] == "POINTSET_MANAGER_ERROR"


def test_api_500_when_pointset_is_corrupted(client, monkeypatch):
    """Un PointSet binaire invalide doit renvoyer 500 (format corrompu)."""

    def fake_get(*_args, **_kwargs):
        # Trop court pour contenir N (uint32)
        return _FakeResponse(200, content=b"\x00\x01")

    app_module = importlib.import_module("triangulator.app")
    monkeypatch.setattr(app_module.requests, "get", fake_get)

    resp = client.get("/triangulation/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 500
    assert resp.get_json()["code"] == "INVALID_POINTSET_FORMAT"
