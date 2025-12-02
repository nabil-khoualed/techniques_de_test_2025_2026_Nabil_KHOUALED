import pytest
from triangulator import triangulation  # module futur

def test_triangulation_triangle_simple():
    """Un triangle simple doit produire un seul triangle."""
    with pytest.raises(NotImplementedError):
        triangulation.compute([(0,0), (1,0), (0,1)])

def test_triangulation_square():
    """Un carré doit produire deux triangles couvrant la surface."""
    with pytest.raises(NotImplementedError):
        triangulation.compute([(0,0), (1,0), (1,1), (0,1)])

def test_points_alignés():
    """Aucun triangle ne doit être formé si tous les points sont alignés."""
    with pytest.raises(NotImplementedError):
        triangulation.compute([(0,0), (1,1), (2,2)])
