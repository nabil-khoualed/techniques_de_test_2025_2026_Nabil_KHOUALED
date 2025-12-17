"""Tests unitaires de la triangulation."""

import pytest

from triangulator import triangulator


def test_triangulation_triangle_simple():
    """Un triangle simple doit produire un seul triangle."""
    triangles = triangulator.compute([(0, 0), (1, 0), (0, 1)])
    assert triangles == [(0, 1, 2)]

def test_triangulation_square():
    """Un carré doit produire deux triangles couvrant la surface."""
    triangles = triangulator.compute([(0, 0), (1, 0), (1, 1), (0, 1)])
    assert len(triangles) == 2

def test_points_alignés():
    """Aucun triangle ne doit être formé si tous les points sont alignés."""
    triangles = triangulator.compute([(0, 0), (1, 1), (2, 2)])
    assert triangles == []


def test_duplicate_points_are_rejected():
    """Des points dupliqués doivent être rejetés (triangulation ambiguë)."""
    with pytest.raises(ValueError):
        triangulator.compute([(0, 0), (1, 0), (1, 0), (0, 1)])
