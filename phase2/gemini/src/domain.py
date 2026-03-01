# src/domain.py
from dataclasses import dataclass
from typing import Tuple, List

# Définition de types personnalisés pour plus de clarté
Point = Tuple[float, float]
Polygon = List[Point]

@dataclass
class VoronoiCell:
    """Représente une cellule du diagramme de Voronoï."""
    site: Point
    polygon: Polygon
    color: str