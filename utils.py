import random
import numpy as np
import sys

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

directions_names = ["UP", "DOWN", "LEFT", "RIGHT"]

# COORDS
X = 1
Y = 0

def generate_random_int(min: int, max: int) -> int:
    return random.randint(min, max)

def handle_ctrl_c(signum, frame):
    sys.exit(0)