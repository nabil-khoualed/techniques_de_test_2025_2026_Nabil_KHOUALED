"""Sérialisation et désérialisation du PointSet.

Format (cf. `point_set_manager.yml`)
---------------------------------

- 4 octets (unsigned long) : nombre de points N
- N * 8 octets : (x, y) en float32

Choix d'implémentation
----------------------

La spécification décrit des *unsigned long* mais ne fige pas explicitement
la taille ni l'endianness. Pour un format stable et interopérable, on fixe :

- entier 32 bits non signé (``uint32``)
- little-endian

Ces choix sont cohérents avec la plupart des formats binaires simples et
facilitent les tests.
"""

from __future__ import annotations

import struct
from collections.abc import Iterable

_U32 = "<I"
_F32 = "<f"


def _ensure_point_tuple(point: object) -> tuple[float, float]:
    """Validate a point ``(x, y)`` and normalize it to ``float``."""
    if not isinstance(point, tuple) or len(point) != 2:
        raise TypeError("Un point doit être un tuple (x, y).")
    x, y = point
    try:
        return float(x), float(y)
    except (TypeError, ValueError) as exc:
        raise TypeError("Les coordonnées doivent être convertibles en float.") from exc

def serialize_pointset(points):
    """Sérialiser un ensemble de points en binaire (format PointSet)."""
    pts = [_ensure_point_tuple(p) for p in points]
    n = len(pts)

    if n > 2**32 - 1:
        raise ValueError("Trop de points pour être encodés en uint32.")

    out = bytearray()
    out += struct.pack(_U32, n)

    for x, y in pts:
        out += struct.pack("<ff", x, y)

    return bytes(out)


def deserialize_pointset(data):
    """Désérialiser un binaire PointSet en liste de points ``(x, y)``."""
    if not isinstance(data, (bytes, bytearray, memoryview)):
        raise TypeError("data doit être un buffer (bytes-like).")

    buf = bytes(data)
    if len(buf) < 4:
        raise ValueError("Données insuffisantes pour lire N.")

    (n,) = struct.unpack_from(_U32, buf, 0)
    expected_len = 4 + (n * 8)
    if len(buf) != expected_len:
        raise ValueError(
            "Longueur invalide: "
            f"attendu {expected_len} octets (N={n}), reçu {len(buf)}."
        )

    points: list[tuple[float, float]] = []
    offset = 4
    for _ in range(n):
        x, y = struct.unpack_from("<ff", buf, offset)
        points.append((x, y))
        offset += 8
    return points


def serialize_triangles(
    points: Iterable[tuple[float, float]],
    triangles: Iterable[tuple[int, int, int]],
) -> bytes:
    """Sérialise une triangulation au format binaire décrit dans `triangulator.yml`.

    Format
    ------
    1) Vertices (= PointSet)
       - uint32 N
       - N * (float32 x, float32 y)
    2) Triangles
       - uint32 T
       - T * (uint32 i0, uint32 i1, uint32 i2)
    """
    pts = [_ensure_point_tuple(p) for p in points]
    tris = [tuple(map(int, t)) for t in triangles]

    n = len(pts)
    if n > 2**32 - 1:
        raise ValueError("Trop de sommets pour être encodés en uint32.")

    for t in tris:
        if len(t) != 3:
            raise ValueError("Un triangle doit avoir 3 indices.")
        if any(i < 0 or i >= n for i in t):
            raise ValueError("Indice de sommet hors bornes dans un triangle.")

    out = bytearray()
    out += struct.pack(_U32, n)
    for x, y in pts:
        out += struct.pack("<ff", x, y)

    out += struct.pack(_U32, len(tris))
    for i0, i1, i2 in tris:
        out += struct.pack("<III", i0, i1, i2)
    return bytes(out)
