import sys, os
import tkinter as tk
from unittest.mock import patch
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.gui import VoronoiApp

def test_scale_points_to_canvas():
    # On instancie Tkinter mais on le cache
    root = tk.Tk()
    root.withdraw() 
    app = VoronoiApp(root)
    
    # Tes fameux points de test : le (0,0) et le maximum (19, 29)
    raw_points = [(0, 0), (10, 15), (19, 29)]
    
    scaled = app._scale_points_to_canvas(raw_points)
    
    assert len(scaled) == 3
    
    # Le point (0,0) doit se retrouver EXACTEMENT à la valeur de la marge (30, 30)
    assert scaled[0] == (30.0, 30.0)
    
    # Le point maximum ne doit pas dépasser (800-30) en X et (600-30) en Y
    assert scaled[2][0] <= 770.0
    assert scaled[2][1] <= 570.0
    
    root.destroy()

def test_clear_and_diagram_state():
    root = tk.Tk()
    root.withdraw()
    app = VoronoiApp(root)
    
    # On simule un état généré
    app.points = [(10, 10)]
    app.diagram_generated = True
    
    # On appelle la fonction de nettoyage
    app.clear()
    
    assert len(app.points) == 0
    assert len(app.cells) == 0
    assert app.diagram_generated is False # Le canevas doit être déverrouillé
    
    root.destroy()