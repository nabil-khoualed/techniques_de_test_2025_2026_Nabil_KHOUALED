"""Tests de performance (smoke tests) du module de triangulation.

Ce ne sont pas des benchmarks, juste une barrière grossière pour détecter une
régression évidente (ex: complexité explosant ou boucle infinie).
"""

from __future__ import annotations

import math
import time

import pytest

from triangulator.triangulator import compute


def _regular_polygon(n: int, radius: float = 1.0) -> list[tuple[float, float]]:
    """Génère un polygone régulier convexe (points sur un cercle)."""
    return [
        (
            radius * math.cos(2.0 * math.pi * i / n),
            radius * math.sin(2.0 * math.pi * i / n),
        )
        for i in range(n)
    ]


@pytest.mark.perf
@pytest.mark.parametrize("n", [100, 500])
def test_triangulation_performance_convex_hull(n: int):
    """La triangulation doit rester rapide sur un polygone convexe."""
    points = _regular_polygon(n)

    start = time.perf_counter()
    triangles = compute(points)
    duration = time.perf_counter() - start

    # Sanity check: un polygone convexe à n sommets a (n-2) triangles.
    assert len(triangles) == n - 2

    # Seuil volontairement large pour éviter les flakes selon machine.
    assert duration < 1.0
