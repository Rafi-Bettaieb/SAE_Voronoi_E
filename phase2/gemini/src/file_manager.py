# src/file_manager.py
from typing import List
from domain import Point, VoronoiCell

class FileManager:
    """Gère l'importation de données et l'exportation de fichiers."""

    @staticmethod
    def load_points(filepath: str) -> List[Point]:
        """Lit un fichier texte/csv et retourne une liste de points."""
        points = []
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.replace(',', ' ').split()
                if len(parts) >= 2:
                    points.append((float(parts[0]), float(parts[1])))
        return points

    @staticmethod
    def export_svg(filepath: str, width: int, height: int, cells: List[VoronoiCell], points: List[Point]) -> None:
        """Génère un fichier vectoriel SVG à partir des cellules calculées."""
        with open(filepath, 'w') as f:
            f.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
            f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">\n')
            
            for cell in cells:
                points_str = " ".join([f"{pt[0]},{pt[1]}" for pt in cell.polygon])
                f.write(f'  <polygon points="{points_str}" fill="{cell.color}" stroke="gray" stroke-width="1" />\n')
            
            for p in points:
                f.write(f'  <circle cx="{p[0]}" cy="{p[1]}" r="3" fill="black" />\n')
                
            f.write('</svg>\n')