# src/gui.py
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import List

from domain import Point, VoronoiCell
from engine import VoronoiEngine
from file_manager import FileManager

class VoronoiApp:
    """Contrôleur de l'interface graphique (Vue)."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Générateur de Diagramme de Voronoï")
        
        self.width = 800
        self.height = 600
        self.points: List[Point] = []
        self.cells: List[VoronoiCell] = []
        
        # Drapeau pour empêcher l'ajout de points après génération
        self.diagram_generated = False 
        
        self.engine = VoronoiEngine(self.width * 2, self.height * 2)
        self._setup_ui()

    def _setup_ui(self):
        """Initialise les widgets Tkinter."""
        control_frame = tk.Frame(self.root, pady=10)
        control_frame.pack(fill=tk.X)
        
        tk.Button(control_frame, text="Charger Points", command=self.load_points).pack(side=tk.LEFT, padx=10)
        tk.Button(control_frame, text="Générer Diagramme", command=self.generate_diagram).pack(side=tk.LEFT, padx=10)
        tk.Button(control_frame, text="Exporter en SVG", command=self.export_svg).pack(side=tk.LEFT, padx=10)
        tk.Button(control_frame, text="Effacer", command=self.clear).pack(side=tk.LEFT, padx=10)
        
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="white", relief=tk.SUNKEN, borderwidth=2)
        self.canvas.pack(padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.add_point_manual)

    def add_point_manual(self, event):
        """Ajoute un point via clic de souris, seulement si le diagramme n'est pas généré."""
        if self.diagram_generated:
            # Si le diagramme est déjà là, on ignore le clic
            return 
            
        self.points.append((event.x, event.y))
        self.canvas.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, fill="black")

    def _scale_points_to_canvas(self, raw_points: List[Point]) -> List[Point]:
        """Adapte les coordonnées brutes pour qu'elles rentrent dans le canevas, ancrées en haut à gauche."""
        if not raw_points:
            return []
            
        # 1. Trouver les vraies limites des données
        min_x = min(p[0] for p in raw_points)
        max_x = max(p[0] for p in raw_points)
        min_y = min(p[1] for p in raw_points)
        max_y = max(p[1] for p in raw_points)
        
        # 2. Calculer la largeur et hauteur des données
        width_data = max(max_x - min_x, 1) # max(..., 1) évite la division par 0
        height_data = max(max_y - min_y, 1)
        
        # La distance (en pixels) par rapport au bord haut et gauche
        margin = 30
        
        # 3. Calculer l'échelle pour que le point le plus lointain ne dépasse pas le cadre
        scale_x = (self.width - (2 * margin)) / width_data
        scale_y = (self.height - (2 * margin)) / height_data
        scale = min(scale_x, scale_y) # Conserver les proportions
        
        # 4. Appliquer la formule : (Valeur - Min) * Echelle + Marge
        # En utilisant "margin" au lieu d'un calcul de centrage, le point (min_x, min_y) 
        # se retrouvera EXACTEMENT au pixel (30, 30), c'est-à-dire en haut à gauche !
        return [((x - min_x) * scale + margin, (y - min_y) * scale + margin) for x, y in raw_points]
    
    def load_points(self):
        """Charge un fichier, met à l'échelle et affiche les points."""
        filepath = filedialog.askopenfilename(
            title="Sélectionner un fichier", 
            filetypes=(("Fichiers texte", "*.txt *.csv"), ("Tous", "*.*"))
        )
        if not filepath: 
            return
            
        try:
            raw_points = FileManager.load_points(filepath)
            if not raw_points:
                return

            # On efface tout pour afficher le nouveau fichier proprement
            self.clear()
            
            scaled_points = self._scale_points_to_canvas(raw_points)
            
            for p in scaled_points:
                self.points.append(p)
                self.canvas.create_oval(p[0]-3, p[1]-3, p[0]+3, p[1]+3, fill="black")
                
            messagebox.showinfo("Succès", f"{len(scaled_points)} points chargés et centrés.")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la lecture:\n{e}")

    def generate_diagram(self):
        """Déclenche le moteur algorithmique et dessine le résultat."""
        if not self.points:
            messagebox.showwarning("Attention", "Veuillez ajouter des points.")
            return
            
        self.canvas.delete("all")
        self.cells = self.engine.compute(self.points)
        
        # Affichage des cellules
        for cell in self.cells:
            flat_poly = [coord for pt in cell.polygon for coord in pt]
            if flat_poly:
                self.canvas.create_polygon(flat_poly, fill=cell.color, outline="gray", width=1)
                
        # Affichage des points (sites) par dessus
        for p in self.points:
            self.canvas.create_oval(p[0]-3, p[1]-3, p[0]+3, p[1]+3, fill="black")
            
        # On verrouille le canevas
        self.diagram_generated = True

    def export_svg(self):
        """Exporte l'affichage actuel au format vectoriel."""
        if not self.cells:
            messagebox.showwarning("Attention", "Générez le diagramme avant d'exporter.")
            return
            
        filepath = filedialog.asksaveasfilename(defaultextension=".svg", filetypes=[("Fichiers SVG", "*.svg")])
        if not filepath: 
            return
            
        try:
            FileManager.export_svg(filepath, self.width, self.height, self.cells, self.points)
            messagebox.showinfo("Succès", "Fichier SVG exporté avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec de l'exportation:\n{e}")

    def clear(self):
        """Réinitialise l'application."""
        self.points.clear()
        self.cells.clear()
        self.canvas.delete("all")
        # On déverrouille le canevas
        self.diagram_generated = False