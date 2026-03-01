import math
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import List, Tuple, Optional
from collections import defaultdict

# ====================== CLASSES ======================
class Vertex:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def equals(self, other: 'Vertex') -> bool:
        return math.isclose(self.x, other.x, abs_tol=1e-9) and math.isclose(self.y, other.y, abs_tol=1e-9)


class Triangle:
    def __init__(self, v0: Vertex, v1: Vertex, v2: Vertex):
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.circumcircle = self._calc_circumcircle()

    def _calc_circumcircle(self):
        ax, ay = self.v0.x, self.v0.y
        bx, by = self.v1.x, self.v1.y
        cx, cy = self.v2.x, self.v2.y
        D = 2 * (ax*(by - cy) + bx*(cy - ay) + cx*(ay - by))
        if abs(D) < 1e-10:
            raise ValueError("Points colinéaires")
        ux = ((ax**2 + ay**2)*(by - cy) + (bx**2 + by**2)*(cy - ay) + (cx**2 + cy**2)*(ay - by)) / D
        uy = ((ax**2 + ay**2)*(cx - bx) + (bx**2 + by**2)*(ax - cx) + (cx**2 + cy**2)*(bx - ax)) / D
        center = Vertex(ux, uy)
        r = math.hypot(ux - ax, uy - ay)
        return {'c': center, 'r': r}

    def in_circumcircle(self, v: Vertex) -> bool:
        dx = self.circumcircle['c'].x - v.x
        dy = self.circumcircle['c'].y - v.y
        return math.hypot(dx, dy) <= self.circumcircle['r'] + 1e-8


# ====================== ALGORITHMES ======================
def super_triangle(points: List[Vertex]) -> Triangle:
    minx = min(p.x for p in points)
    miny = min(p.y for p in points)
    maxx = max(p.x for p in points)
    maxy = max(p.y for p in points)
    dx = maxx - minx
    dy = maxy - miny
    return Triangle(
        Vertex(minx - 3*dx, miny - 3*dy),
        Vertex(maxx + 3*dx, miny - 3*dy),
        Vertex(maxx, maxy + 3*dy)
    )


def delaunay_triangulate(points: List[Vertex]) -> List[Triangle]:
    if len(points) < 3:
        raise ValueError("Au moins 3 points sont requis.")
    unique = []
    for p in points:
        if not any(p.equals(u) for u in unique):
            unique.append(p)
    points = unique

    st = super_triangle(points)
    triangles = [st]

    for p in points:
        bad = [t for t in triangles if t.in_circumcircle(p)]
        edge_count = defaultdict(int)
        for t in bad:
            for e in [(t.v0, t.v1), (t.v1, t.v2), (t.v2, t.v0)]:
                key = tuple(sorted(e, key=id))
                edge_count[key] += 1
        polygon = [Edge(e[0], e[1]) for e, cnt in edge_count.items() if cnt == 1]  # Edge class manquante → ajoutée ci-dessous

        remaining = [t for t in triangles if t not in bad]
        new_tri = []
        for e in polygon:
            try:
                new_tri.append(Triangle(e.v0, e.v1, p))
            except ValueError:
                pass
        triangles = remaining + new_tri

    st_set = {st.v0, st.v1, st.v2}
    triangles = [t for t in triangles if not {t.v0, t.v1, t.v2} & st_set]
    return triangles


class Edge:
    def __init__(self, v0: Vertex, v1: Vertex):
        self.v0 = v0
        self.v1 = v1


def compute_voronoi_edges(triangles: List[Triangle], points: List[Vertex]) -> List[Tuple[Vertex, Vertex]]:
    """Version corrigée : direction des rayons infinis parfaitement outward"""
    edge_to_tris = defaultdict(list)
    for t in triangles:
        for pair in [(t.v0, t.v1), (t.v1, t.v2), (t.v2, t.v0)]:
            key = tuple(sorted(pair, key=id))
            edge_to_tris[key].append(t)

    vor_edges = []
    ray_length = 5000.0

    for key, tris in edge_to_tris.items():
        p, q = key
        if len(tris) == 2:
            c1 = tris[0].circumcircle['c']
            c2 = tris[1].circumcircle['c']
            if not c1.equals(c2):
                vor_edges.append((c1, c2))

        elif len(tris) == 1:
            t = tris[0]
            c = t.circumcircle['c']
            third = next(v for v in (t.v0, t.v1, t.v2) if v is not p and v is not q)

            mx = (p.x + q.x) / 2.0
            my = (p.y + q.y) / 2.0

            dx = q.x - p.x
            dy = q.y - p.y

            # Deux directions perpendiculaires
            px1, py1 = -dy, dx
            px2, py2 = dy, -dx

            # Choisir celle qui pointe vers l'extérieur (opposé au troisième point)
            vec_to_third_x = third.x - mx
            vec_to_third_y = third.y - my
            dot1 = px1 * vec_to_third_x + py1 * vec_to_third_y

            px, py = (px1, py1) if dot1 < 0 else (px2, py2)

            length = math.hypot(px, py)
            if length > 1e-8:
                px /= length
                py /= length
                far = Vertex(c.x + px * ray_length, c.y + py * ray_length)
                vor_edges.append((c, far))

    return vor_edges


# ====================== CLIPPING + CHARGEMENT ======================
def clip_line(x1, y1, x2, y2, xmin, ymin, xmax, ymax) -> Optional[Tuple[float, float, float, float]]:
    def outcode(x, y):
        code = 0
        if x < xmin: code |= 1
        if x > xmax: code |= 2
        if y < ymin: code |= 4
        if y > ymax: code |= 8
        return code

    oc1 = outcode(x1, y1)
    oc2 = outcode(x2, y2)
    while True:
        if not (oc1 | oc2):
            return x1, y1, x2, y2
        if oc1 & oc2:
            return None
        oc = oc1 if oc1 else oc2
        if oc & 8:
            x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
            y = ymax
        elif oc & 4:
            x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
            y = ymin
        elif oc & 2:
            y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
            x = xmax
        elif oc & 1:
            y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
            x = xmin
        if oc == oc1:
            x1, y1, oc1 = x, y, outcode(x, y)
        else:
            x2, y2, oc2 = x, y, outcode(x, y)


def load_points_from_file(filename: str) -> List[Vertex]:
    points = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.replace(' ', ',').split(',')
            parts = [p.strip() for p in parts if p.strip()]
            if len(parts) == 2:
                try:
                    points.append(Vertex(float(parts[0]), float(parts[1])))
                except ValueError:
                    pass
    return points


# ====================== INTERFACE ======================
class VoronoiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Diagramme de Voronoï - Version Finale")
        self.root.geometry("940x780")

        self.canvas = tk.Canvas(root, width=900, height=700, bg="#f8f9fa", highlightthickness=0)
        self.canvas.pack(pady=10)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=8)

        tk.Button(btn_frame, text="Charger fichier points (.txt)", 
                  command=self.load_file, width=28, height=2).pack(side=tk.LEFT, padx=15)
        self.export_btn = tk.Button(btn_frame, text="Exporter en SVG", 
                                    command=self.export_svg, state=tk.DISABLED, width=28, height=2)
        self.export_btn.pack(side=tk.LEFT, padx=15)

        self.points: List[Vertex] = []
        self.vor_edges: List[Tuple[Vertex, Vertex]] = []

    def load_file(self):
        file = filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt")])
        if not file:
            return
        try:
            self.points = load_points_from_file(file)
            if len(self.points) < 3:
                raise ValueError("Le fichier doit contenir au moins 3 points.")

            triangles = delaunay_triangulate(self.points)
            self.vor_edges = compute_voronoi_edges(triangles, self.points)

            self.draw_diagram()
            self.export_btn.config(state=tk.NORMAL)
            messagebox.showinfo("Succès", f"{len(self.points)} points → Diagramme correct !")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def draw_diagram(self):
        self.canvas.delete("all")
        if not self.points:
            return

        xs = [p.x for p in self.points]
        ys = [p.y for p in self.points]
        minx, maxx = min(xs), max(xs)
        miny, maxy = min(ys), max(ys)
        pad = max(maxx-minx, maxy-miny) * 0.22
        xmin, xmax = minx - pad, maxx + pad
        ymin, ymax = miny - pad, maxy + pad

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        scale = min((w-60)/(xmax-xmin), (h-60)/(ymax-ymin))
        ox = 30 - xmin * scale
        oy = 30 - ymin * scale

        for v1, v2 in self.vor_edges:
            clipped = clip_line(v1.x, v1.y, v2.x, v2.y, xmin, ymin, xmax, ymax)
            if clipped:
                x1, y1, x2, y2 = clipped
                self.canvas.create_line(
                    x1*scale + ox, y1*scale + oy,
                    x2*scale + ox, y2*scale + oy,
                    fill="#2c3e50", width=2.2
                )

        for p in self.points:
            x = p.x * scale + ox
            y = p.y * scale + oy
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="#e74c3c", outline="#2c3e50", width=1.5)

    def export_svg(self):
        if not self.points:
            return
        file = filedialog.asksaveasfilename(defaultextension=".svg", filetypes=[("SVG", "*.svg")])
        if file:
            # Même logique d'export que le dessin
            xs = [p.x for p in self.points]
            ys = [p.y for p in self.points]
            minx, maxx = min(xs), max(xs)
            miny, maxy = min(ys), max(ys)
            pad = max(maxx-minx, maxy-miny) * 0.22
            xmin, xmax = minx - pad, maxx + pad
            ymin, ymax = miny - pad, maxy + pad

            w = 920
            h = 720
            scale = min((w-60)/(xmax-xmin), (h-60)/(ymax-ymin))
            ox = 30 - xmin * scale
            oy = 30 - ymin * scale

            with open(file, 'w', encoding='utf-8') as f:
                f.write(f'<svg width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">\n')
                f.write('<rect width="100%" height="100%" fill="#f8f9fa"/>\n')
                for v1, v2 in self.vor_edges:
                    clipped = clip_line(v1.x, v1.y, v2.x, v2.y, xmin, ymin, xmax, ymax)
                    if clipped:
                        x1, y1, x2, y2 = clipped
                        x1 = x1*scale + ox
                        y1 = y1*scale + oy
                        x2 = x2*scale + ox
                        y2 = y2*scale + oy
                        f.write(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
                                f'stroke="#2c3e50" stroke-width="2.2"/>\n')
                for p in self.points:
                    x = p.x * scale + ox
                    y = p.y * scale + oy
                    f.write(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5" fill="#e74c3c" stroke="#2c3e50"/>\n')
                f.write('</svg>\n')
            messagebox.showinfo("Export terminé", f"Sauvegardé :\n{file}")


if __name__ == "__main__":
    root = tk.Tk()
    app = VoronoiApp(root)
    root.mainloop()