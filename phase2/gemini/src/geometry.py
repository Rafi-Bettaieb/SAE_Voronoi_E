# src/geometry.py
from domain import Point

class Geometry:
    """Classe regroupant les opérations de géométrie vectorielle 2D."""

    @staticmethod
    def dot_product(v1: Point, v2: Point) -> float:
        return v1[0] * v2[0] + v1[1] * v2[1]

    @staticmethod
    def subtract(p1: Point, p2: Point) -> Point:
        return (p1[0] - p2[0], p1[1] - p2[1])

    @staticmethod
    def add(p1: Point, p2: Point) -> Point:
        return (p1[0] + p2[0], p1[1] + p2[1])

    @staticmethod
    def multiply(p: Point, scalar: float) -> Point:
        return (p[0] * scalar, p[1] * scalar)

    @staticmethod
    def is_inside(p: Point, p0: Point, n: Point) -> bool:
        """Vérifie si le point 'p' est du bon côté du demi-plan défini par (p0, normale n)."""
        return Geometry.dot_product(Geometry.subtract(p, p0), n) >= 0

    @staticmethod
    def intersect(v1: Point, v2: Point, p0: Point, n: Point) -> Point:
        """Calcule l'intersection exacte entre le segment [v1, v2] et la droite (p0, n)."""
        d1 = Geometry.dot_product(Geometry.subtract(v1, p0), n)
        d2 = Geometry.dot_product(Geometry.subtract(v2, p0), n)
        
        if d1 - d2 == 0:
            return v1
            
        t = d1 / (d1 - d2)
        diff = Geometry.subtract(v2, v1)
        return Geometry.add(v1, Geometry.multiply(diff, t))