# src/main.py
import tkinter as tk
from gui import VoronoiApp

def main():
    root = tk.Tk()
    app = VoronoiApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()