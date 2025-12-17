"""Fonctions de calcul de triangulation.

Ce module sera complété lors de la dernière séance pour produire
le binaire des triangles décrit dans triangulator.yml.
"""

from __future__ import annotations


def _cross(
    o: tuple[float, float],
    a: tuple[float, float],
    b: tuple[float, float],
) -> float:
    """Produit vectoriel (OA x OB), positif si virage à gauche."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def _convex_hull_indices(points: list[tuple[float, float]]) -> list[int]:
    """Renvoie les indices des points sur l'enveloppe convexe.

    Si tous les points sont colinéaires, l'enveloppe contient seulement les extrémités
    (ou 0/1 point si l'entrée est dégénérée).
    """
    indexed = list(enumerate(points))
    indexed.sort(key=lambda it: (it[1][0], it[1][1]))
    if len(indexed) <= 1:
        return [i for i, _ in indexed]

    def build_half(pts: list[tuple[int, tuple[float, float]]]) -> list[int]:
        half: list[int] = []
        for idx, p in pts:
            while len(half) >= 2:
                p1 = points[half[-2]]
                p2 = points[half[-1]]
                if _cross(p1, p2, p) <= 0:
                    half.pop()
                else:
                    break
            half.append(idx)
        return half

    lower = build_half(indexed)
    upper = build_half(list(reversed(indexed)))
    hull = lower[:-1] + upper[:-1]

    # Dé-dup (peut arriver en cas de colinéarité)
    seen: set[int] = set()
    out: list[int] = []
    for i in hull:
        if i not in seen:
            out.append(i)
            seen.add(i)
    return out


def _is_colinear(points: list[tuple[float, float]]) -> bool:
    if len(points) < 3:
        return True
    o = points[0]
    # trouve un point différent
    i = 1
    while i < len(points) and points[i] == o:
        i += 1
    if i == len(points):
        return True
    a = points[i]
    return all(_cross(o, a, b) == 0 for b in points[i + 1 :])

def compute(points):
    """Compute a deterministic triangulation for a list of points (convex cases)."""
    pts = [tuple(map(float, p)) for p in points]

    if len(set(pts)) != len(pts):
        raise ValueError("Points dupliqués: la triangulation est ambiguë.")

    if len(pts) < 3 or _is_colinear(pts):
        return []

    hull = _convex_hull_indices(pts)
    if len(hull) < 3:
        return []

    # Triangulation en éventail: (h0, h[i], h[i+1])
    h0 = hull[0]
    triangles: list[tuple[int, int, int]] = []
    for i in range(1, len(hull) - 1):
        triangles.append((h0, hull[i], hull[i + 1]))
    return triangles
