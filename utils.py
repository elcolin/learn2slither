import random
import numpy as np

# ITEMS

WALL = 'W'
SNAKE_HEAD = 'H'
SNAKE_BODY = 'S'
GREEN_APPLE = 'G'
RED_APPLE = 'R'
EMPTY = '0'

UP : tuple[int, int] = (-1, 0)
DOWN : tuple[int, int] = (1, 0)
LEFT : tuple[int, int] = (0, -1)
RIGHT : tuple[int, int] = (0, 1)

directions: list[tuple[int, int]] = [UP, DOWN, LEFT, RIGHT]

CELL_SIZE = 40  # taille de chaque cellule en pixels

directions_names = ["UP", "DOWN", "LEFT", "RIGHT"]

colors = {
    'W': 'black',   # murs
    '0': 'white',   # vide
    'H': 'darkgreen', # tête serpent
    'S': 'green',     # corps serpent
    'G': 'lightgreen',# pomme verte
    'R': 'red'        # pomme rouge
}
# COORDS
X = 1
Y = 0

def generate_random(min: int, max: int) -> int:
    return random.randint(min, max)
