import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import re
from src.engine import VoronoiEngine

def test_clip_polygon():
    engine = VoronoiEngine(100, 100)
    # Un carré de 20x20 centré sur l'origine
    poly = [(-10, -10), (10, -10), (10, 10), (-10, 10)]
    
    # On le coupe en deux avec l'axe Y (on garde la partie droite)
    p0 = (0, 0)
    n = (1, 0) 
    
    clipped = engine._clip_polygon(poly, p0, n)
    
    # Le polygone résultant doit être la moitié droite (0 à 10 en X)
    assert len(clipped) == 4
    # Les nouveaux points X doivent être >= 0
    assert all(p[0] >= 0 for p in clipped)

def test_compute():
    engine = VoronoiEngine(800, 600)
    points = [(10, 10), (20, 20)]
    
    cells = engine.compute(points)
    
    assert len(cells) == 2
    assert cells[0].site in points
    assert len(cells[0].polygon) > 0

def test_random_color():
    engine = VoronoiEngine(800, 600)
    color = engine._random_pastel_color()
    # Vérifie que c'est un code hexadécimal valide (ex: #a2b4c6)
    assert re.match(r"^#[0-9a-f]{6}$", color)