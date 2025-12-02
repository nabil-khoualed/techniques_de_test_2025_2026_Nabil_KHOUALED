import pytest
from triangulator import binary  # fichier qui n’existe pas encore → normal

def test_serialize_empty_pointset():
    """Un ensemble vide doit produire un binaire valide (4 octets = nombre de points = 0)."""
    with pytest.raises(NotImplementedError):
        binary.serialize_pointset([])

def test_serialize_one_point():
    """Un point doit être converti correctement en binaire (à implémenter plus tard)."""
    with pytest.raises(NotImplementedError):
        binary.serialize_pointset([(1.0, 2.0)])

def test_deserialize_invalid_data():
    """Un format incorrect doit déclencher une erreur."""
    with pytest.raises(Exception):
        binary.deserialize_pointset(b"abc")  # données invalides
