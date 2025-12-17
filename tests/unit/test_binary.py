"""Tests unitaires du module `triangulator.binary`."""

import struct

import pytest

from triangulator import binary


def test_serialize_empty_pointset():
    """Un ensemble vide produit un binaire valide (N=0)."""
    data = binary.serialize_pointset([])
    assert data == struct.pack("<I", 0)

def test_serialize_one_point():
    """Un point doit être converti correctement en binaire (à implémenter plus tard)."""
    data = binary.serialize_pointset([(1.0, 2.0)])
    assert data == struct.pack("<Iff", 1, 1.0, 2.0)

def test_deserialize_invalid_data():
    """Un format incorrect doit déclencher une erreur."""
    with pytest.raises(ValueError):
        binary.deserialize_pointset(b"abc")  # données invalides


def test_deserialize_requires_bytes_like():
    """Le décodeur doit refuser les entrées non bytes-like."""
    with pytest.raises(TypeError):
        binary.deserialize_pointset("not-bytes")  # type: ignore[arg-type]


def test_serialize_pointset_rejects_bad_point_shape():
    """Un point doit être un tuple (x, y)."""
    with pytest.raises(TypeError):
        binary.serialize_pointset([(1.0, 2.0, 3.0)])  # type: ignore[list-item]


def test_serialize_pointset_rejects_non_numeric_coordinates():
    """Les coordonnées doivent être convertibles en float."""
    with pytest.raises(TypeError):
        binary.serialize_pointset([("x", "y")])


def test_serialize_triangles_rejects_wrong_triangle_arity():
    """Un triangle doit avoir exactement 3 indices."""
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    with pytest.raises(ValueError):
        binary.serialize_triangles(points, [(0, 1)])  # type: ignore[list-item]


def test_serialize_triangles_rejects_out_of_bounds_index():
    """Les indices de triangle doivent référencer un sommet existant."""
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    with pytest.raises(ValueError):
        binary.serialize_triangles(points, [(0, 1, 3)])
