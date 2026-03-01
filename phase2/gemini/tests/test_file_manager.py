import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.file_manager import FileManager
from src.domain import VoronoiCell

def test_load_points(tmp_path):
    # Création d'un faux fichier texte
    file_path = tmp_path / "test_points.txt"
    file_path.write_text("10, 20\n30.5 40.2\n# Ceci est un commentaire\n50,60")
    
    points = FileManager.load_points(str(file_path))
    
    assert len(points) == 3
    assert points[0] == (10.0, 20.0)
    assert points[1] == (30.5, 40.2)
    assert points[2] == (50.0, 60.0)

def test_export_svg(tmp_path):
    # Création de données bidons
    cells = [VoronoiCell(site=(10, 10), polygon=[(0,0), (20,0), (20,20)], color="#ff0000")]
    points = [(10, 10)]
    
    # Export
    file_path = tmp_path / "output.svg"
    FileManager.export_svg(str(file_path), 800, 600, cells, points)
    
    # Vérification que le fichier existe et contient les bonnes balises
    assert file_path.exists()
    content = file_path.read_text()
    assert "<svg" in content
    assert "<polygon" in content
    assert "<circle" in content