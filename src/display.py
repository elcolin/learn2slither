import tkinter as tk
import numpy as np
from typing import Optional
from utils import *
CELL_SIZE = 40  # taille de chaque cellule en pixels

colors = {
    'W': 'black',   # murs
    '0': 'white',   # vide
    'H': 'darkgreen', # tête serpent
    'S': 'green',     # corps serpent
    'G': 'lightgreen',# pomme verte
    'R': 'red'        ,# pomme rouge
    'Y': 'yellow'
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
        width = MAP_SIZE * 40
        self.root.geometry(f"{width}x{width}")  # optionnel : taille en pixels
        self.canvas = tk.Canvas(self.root, width=MAP_SIZE * 40, height=MAP_SIZE * 40)
        self.canvas.pack()

    def draw_rectangle(self, coords: tuple[int, int], color: str):
         
        if (self.canvas is None):
            return
        x1, y1 = coords[X] * CELL_SIZE, coords[Y] * CELL_SIZE
        x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
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
