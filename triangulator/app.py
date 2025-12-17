"""Application Flask principale du Triangulator.

Cette application expose l’endpoint `/triangulation/<pointset_id>` décrit dans
la spécification OpenAPI `triangulator.yml`.

La logique de récupération du PointSet, son décodage, la triangulation et
l'encodage du résultat seront implémentés lors de la dernière séance.
"""

from __future__ import annotations

import os
import uuid

import requests
from flask import Flask, Response, jsonify

from triangulator.binary import deserialize_pointset, serialize_triangles
from triangulator.triangulator import compute

app = Flask(__name__)


def _point_set_manager_base_url() -> str:
    """Retourne l'URL de base du PointSetManager.

    Peut être configurée via la variable d'environnement `POINT_SET_MANAGER_URL`.
    """
    return os.environ.get("POINT_SET_MANAGER_URL", "http://localhost:8000").rstrip("/")


def _error(status: int, code: str, message: str) -> tuple[Response, int]:
    return jsonify({"code": code, "message": message}), status

@app.get("/triangulation/<pointset_id>")
def triangulate(pointset_id):
    """Compute a triangulation (binary) from a ``PointSetID`` (UUID)."""
    try:
        uuid.UUID(pointset_id)
    except ValueError:
        return _error(400, "INVALID_POINTSET_ID", "Le pointSetId doit être un UUID.")

    url = f"{_point_set_manager_base_url()}/pointset/{pointset_id}"
    try:
        resp = requests.get(url, timeout=2)
    except requests.RequestException:
        return _error(
            503,
            "POINTSET_MANAGER_UNAVAILABLE",
            "PointSetManager injoignable.",
        )

    if resp.status_code == 404:
        return _error(404, "NOT_FOUND", "PointSet introuvable.")
    if resp.status_code == 400:
        return _error(400, "BAD_REQUEST", "Requête invalide auprès du PointSetManager.")
    if resp.status_code >= 500:
        return _error(
            503,
            "POINTSET_MANAGER_UNAVAILABLE",
            "PointSetManager indisponible.",
        )
    if resp.status_code != 200:
        return _error(
            503,
            "POINTSET_MANAGER_ERROR",
            "Réponse inattendue du PointSetManager.",
        )

    try:
        points = deserialize_pointset(resp.content)
    except ValueError:
        return _error(500, "INVALID_POINTSET_FORMAT", "PointSet corrompu ou invalide.")

    try:
        triangles = compute(points)
        out = serialize_triangles(points, triangles)
    except ValueError as exc:
        return _error(500, "TRIANGULATION_FAILED", str(exc))
    except Exception:
        return _error(500, "TRIANGULATION_FAILED", "Triangulation impossible.")

    return Response(out, status=200, content_type="application/octet-stream")
