PLAN – Techniques de Test

1. Introduction

Le but de ce TP est d’apprendre à concevoir et organiser des tests sur un petit service appelé Triangulator.
Ce service reçoit un ensemble de points en 2D, calcule des triangles à partir de ces points,
et renvoie le résultat au client sous forme binaire.

Le but principal n’est pas d’avoir un algorithme parfait,
mais de mettre en place des tests variés et pertinents pour valider le bon fonctionnement du code.

2. Fonctionnement du Triangulator

Le Triangulator reçoit un identifiant (pointSetId) et contacte un autre service,
le PointSetManager, pour récupérer les points associés.
Ensuite, il calcule les triangles correspondants et renvoie le résultat au client.

Le format échangé est binaire :

Pour un PointSet :
  4 octets → nombre de points, puis 8 octets par point (X et Y).
Pour un Triangles :
  même structure pour les points, plus une partie décrivant les indices des triangles.


3. Données de test prévues

Pour concevoir les tests, plusieurs ensembles de points seront utilisés :

| Cas              | Description             | Résultat attendu                              |
|------------------|-------------------------|-----------------------------------------------|
| Aucun point      | Ensemble vide           | Pas d’erreur, 0 triangle                      |
| 3 points         | Triangle simple         | 1 triangle formé                              |
| 4 points         | Carré                   | 2 triangles couvrant la surface               |
| Points doublés   | Deux points identiques  | Erreur ou message clair                       |
| Points alignés   | Tous sur la même ligne  | Aucun triangle formé                          |
| Données invalides| Format binaire corrompu | Erreur de format gérée proprement             |


4. Types de tests
a) Tests unitaires

Tester les fonctions internes, par exemple :

Conversion entre les structures Python et le format binaire (PointSet ↔ bytes).
Vérification que la triangulation fonctionne sur des petits ensembles.
Gestion correcte des cas particuliers (0 point, points doublés, alignés…).

b) Tests d’intégration

Vérifier le fonctionnement global du service :

Simulation du PointSetManager avec des mocks pour imiter ses réponses.
Test complet : récupérer les points → calculer → renvoyer le résultat.

c) Tests d’API

Tester la route /triangulation/{pointSetId} avec le client Flask :

200 OK : quand tout se passe bien.
400 : si l’ID est invalide ou les données mal formées.
404 : si le PointSet n’existe pas.
503 : si le PointSetManager est indisponible.

d) Tests de performance

Mesurer le temps de calcul pour des ensembles de 100, 1 000 ou 10 000 points.
Vérifier que le temps reste raisonnable et ne provoque pas d’erreurs mémoire.

e) Tests de robustesse

Envoyer des données incomplètes ou corrompues.
Vérifier que le service ne plante pas et renvoie un message d’erreur clair.

5. Outils utilisés

pytest → exécution des tests
coverage → taux de couverture du code
ruff → contrôle de la qualité et des docstrings
pdoc3 → documentation automatique
make → simplification des commandes (make test, make lint, make doc, etc.)



6. Objectif final

Avoir un projet :

propre et bien structuré, avec des tests clairs couvrant les cas normaux et les erreurs, et un code de qualité facile à maintenir.

Le but est de montrer une bonne démarche de test, plus que d’avoir un algorithme complexe ou une application complète.
