# RETEX – Triangulator (TP Techniques de Test)

## Contexte

Ce TP consistait à développer un micro-service de triangulation (Triangulator)
exposé via une API HTTP, et à construire un dispositif de tests (unitaires,
intégration, API, performance) capable de guider l’implémentation et de fournir
des garanties sur la qualité.

## Ce qui a bien fonctionné

### Démarche orientée tests

- Avoir écrit un plan de tests (`PLAN.md`) m’a forcé à **identifier les cas** avant
	de coder : ensembles vides, points alignés, formats binaires corrompus, etc.
- La séparation en répertoires **unit / integration / perf** sous `tests/` rend la
	suite lisible, et colle bien à l’idée “pyramide de tests”.

### Contrats simples et vérifiables

- Définir des formats binaires simples (compteurs + couples float32) a permis
	d’écrire des assertions très concrètes (taille, entêtes, etc.).
- Le fait d’encoder correctement les erreurs HTTP (400/404/503/500) rend l’API
	plus facile à tester et plus robuste vis-à-vis d’un service externe.

### Checks de qualité

- L’usage de `ruff` a rapidement mis en évidence des problèmes récurrents
	(imports inutilisés, style de docstrings, etc.). Ça évite l’accumulation de dette
	technique.

## Ce qui a moins bien fonctionné

### Hypothèses initiales trop floues

- La spécification parle d’unsigned long, mais ne fixe pas clairement la taille
	ni l’endianness. Au début, j’avais sous-estimé ce point.
	Résultat : il faut trancher (ici: uint32 little-endian) et documenter ce choix.

### Tests placeholder à réécrire

- Les premiers tests attendaient des `NotImplementedError`. C’est pratique pour
	la séance "setup", mais cela doit être **refactoré** en assertions métier à la fin.
	Cette évolution est normale mais prend du temps si on ne l’anticipe pas.

### Triangulation: complexité sous-estimée

- Faire une triangulation générale (Delaunay, contraintes, cas dégénérés) est
	un sujet en soi. Pour un TP d’ingénierie de test, l’important était surtout de
	choisir un algorithme **déterministe** assez simple pour être testable.
- L’implémentation finale fait une triangulation en éventail à partir de l’enveloppe
	convexe : ce n’est pas optimal ni universel, mais c’est stable, rapide et adapté
	aux jeux de tests (triangle/carré).

## Ce que je ferais différemment

1. **Écrire un contrat formel** dès le début (entrées/sorties, erreurs, format
	 exact binaire, endianness). Même quelques lignes dans le README auraient réduit
	 les ambiguïtés.
2. Ajouter plus tôt des tests de non-régression sur les cas limites :
	 - points dupliqués
	 - "presque" colinéaires (tolérance flottante)
	 - PointSet très grand (mémoire / temps)
3. Mettre en place un petit outil de génération de PointSet "réalistes" pour
	 alimenter les tests perf et robustesse.

## Bilan par rapport au plan initial (`PLAN.md`)

- Le plan était globalement pertinent (unit, intégration, API, perf).
- La partie la plus “optimiste” était la triangulation elle-même : il faut réduire
	l’ambition de l’algorithme (ou accepter d’y passer beaucoup plus de temps).
- Les tests d’intégration avec mocks se sont révélés essentiels : ils permettent
	de tester le Triangulator **sans dépendre** d’un PointSetManager réellement lancé.

## Conclusion

Le TP montre bien que la valeur principale d’une approche test-first est de
clarifier le comportement attendu et de rendre l’implémentation itérative.
Les tests ont aussi servi de "documentation exécutable" et ont guidé les choix
techniques (format binaire stable, erreurs API explicites, algorithme déterministe).
