"""Package principal du Triangulator.

Ce package expose les modules nécessaires au fonctionnement de l'application :
- app : point d'entrée de l’API Flask
- binary : sérialisation/désérialisation du PointSet (implémenté plus tard)
- triangulation : calcul de la triangulation (implémenté plus tard)
"""

from .app import app as app

__all__ = ["app"]
