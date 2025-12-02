"""
Application Flask principale du Triangulator.

Cette application expose l’endpoint `/triangulation/<pointset_id>` décrit dans
la spécification OpenAPI `triangulator.yml`.

La logique de récupération du PointSet, son décodage, la triangulation et
l'encodage du résultat seront implémentés lors de la dernière séance.
"""

from flask import Flask

app = Flask(__name__)

@app.get("/triangulation/<pointset_id>")
def triangulate(pointset_id):
    """
    Point d'entrée de l'API pour calculer une triangulation.

    Parameters
    ----------
    pointset_id : str
        Identifiant du PointSet à récupérer auprès du PointSetManager.

    Returns
    -------
    tuple
        Une réponse HTTP indiquant que la logique n'est pas encore implémentée.

    Notes
    -----
    La réponse actuelle est volontairement un HTTP 501 (Not Implemented),
    conformément au fait que la logique du Triangulator n'est pas encore écrite.
    """
    return "Not implemented", 501
