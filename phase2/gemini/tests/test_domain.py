import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.domain import VoronoiCell

def test_voronoi_cell_creation():
    """Vérifie la création correcte d'un objet VoronoiCell."""
    site = (15.5, 20.0)
    poly = [(0, 0), (10, 0), (10, 10), (0, 10)]
    color = "#aabbcc"
    
    cell = VoronoiCell(site=site, polygon=poly, color=color)
    
    assert cell.site == (15.5, 20.0)
    assert len(cell.polygon) == 4
    assert cell.color == "#aabbcc"