# Lance tous les tests (basé sur pytest)
test:
	pytest -v

# Lance tous les tests sauf les tests de performance (basé sur pytest)
unit_test:
	pytest -v -m "not perf"

# Lance uniquement les tests de performance (basé sur pytest)
perf_test:
	pytest -v -m perf

# Génère un rapport de couverture de code (basé sur coverage)
coverage:
	coverage run -m pytest -m "not perf"
	coverage report -m

# Valide la qualité de code (basé sur ruff check)
lint:
	ruff check .

# Génère la documentation en HTML (basé sur pdoc3)
doc:
	pdoc3 --force --html triangulator
