import tkinter as tk
import numpy as np
from typing import Optional
CELL_SIZE = 40  # taille de chaque cellule en pixels

colors = {
    'W': 'black',   # murs
    '0': 'white',   # vide
    'H': 'darkgreen', # tête serpent
    'S': 'green',     # corps serpent
    'G': 'lightgreen',# pomme verte
    'R': 'red'        # pomme rouge
}

class DisplayGame:
    def __init__(self, display_activated: bool = True):
        self.display_activated_ = display_activated
        self.root = tk.Tk()
        self.canvas : Optional[tk.Canvas] = None
        if (display_activated == False):
            self.root.withdraw()
            return
        self.root.title("Snake")
        self.root.geometry("400x400")  # optionnel : taille en pixels
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

    def draw_grid(self, grid: np.array):
        if (not self.display_activated_):
            return
        self.canvas.delete("all")
        for r in range(grid.shape[0]):
            for c in range(grid.shape[1]):
                x1, y1 = c * CELL_SIZE, r * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                cell_value = grid[r, c]
                color = colors.get(cell_value, "white")
                if (self.canvas):
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
    def set_timer_callback(self, time , func):
            self.root.after(time, func)
    def set_callback(self, func):
        if (self.display_activated_):
            self.root.after(100, func)
            return
        self.root.after_idle(func)
