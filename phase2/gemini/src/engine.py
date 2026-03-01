# src/engine.py
import random
from typing import List
from domain import Point, Polygon, VoronoiCell
from geometry import Geometry

class VoronoiEngine:
    """Moteur de calcul du diagramme de Voronoï par intersection de demi-plans."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # Boîte englobante virtuelle infinie (très grande)
        self.base_bbox: Polygon = [
            (-width, -height),
            (width * 2, -height),
            (width * 2, height * 2),
            (-width, height * 2)
        ]

    def _clip_polygon(self, poly: Polygon, p0: Point, n: Point) -> Polygon:
        """Algorithme de Sutherland-Hodgman pour découper un polygone."""
        if not poly:
            return []
        
        clipped = []
        for i in range(len(poly)):
            v1 = poly[i]
            v2 = poly[(i + 1) % len(poly)]
            
            v1_in = Geometry.is_inside(v1, p0, n)
            v2_in = Geometry.is_inside(v2, p0, n)
            
            if v1_in and v2_in:
                clipped.append(v2)
            elif v1_in and not v2_in:
                clipped.append(Geometry.intersect(v1, v2, p0, n))
            elif not v1_in and v2_in:
                clipped.append(Geometry.intersect(v1, v2, p0, n))
                clipped.append(v2)
                
        return clipped

    def compute(self, points: List[Point]) -> List[VoronoiCell]:
        """Génère les cellules de Voronoï pour un ensemble de sites donnés."""
        cells = []
        unique_points = list(set(points)) # Suppression des doublons
        
        for i, p in enumerate(unique_points):
            poly = self.base_bbox[:]
            for j, other in enumerate(unique_points):
                if i == j:
                    continue
                
                midpoint = Geometry.multiply(Geometry.add(p, other), 0.5)
                normal = Geometry.subtract(p, other)
                poly = self._clip_polygon(poly, midpoint, normal)
                
            color = self._random_pastel_color()
            cells.append(VoronoiCell(site=p, polygon=poly, color=color))
            
        return cells

    def _random_pastel_color(self) -> str:
        """Génère une couleur hexadécimale pastel."""
        r, g, b = random.randint(150, 255), random.randint(150, 255), random.randint(150, 255)
        return f"#{r:02x}{g:02x}{b:02x}"