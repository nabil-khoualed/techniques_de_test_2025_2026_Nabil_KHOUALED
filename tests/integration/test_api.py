import pytest
from triangulator.app import app

@pytest.fixture
def client():
    return app.test_client()

def test_get_triangulation_returns_501():
    """L’API doit renvoyer 501 tant que la logique n'est pas implémentée."""
    response = client().get("/triangulation/testid")
    assert response.status_code == 501

def test_invalid_id_format():
    """Un ID invalide devrait produire une erreur (plus tard)."""
    with pytest.raises(NotImplementedError):
        raise NotImplementedError("Logique non implémentée pour le moment")
