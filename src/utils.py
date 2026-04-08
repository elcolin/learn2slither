import random
import numpy as np

WALL = 'W'
SNAKE_HEAD = 'H'
SNAKE_BODY = 'S'
GREEN_APPLE = 'G'
RED_APPLE = 'R'
EMPTY = '0'

MAP_SIZE = 10
NUMBER_OF_GREEN_APPLE = 2
NUMBER_OF_RED_APPLE = 1

UP : tuple[int, int] = (-1, 0)
DOWN : tuple[int, int] = (1, 0)
LEFT : tuple[int, int] = (0, -1)
RIGHT : tuple[int, int] = (0, 1)

directions: list[tuple[int, int]] = [UP, DOWN, RIGHT, LEFT]

# opposite_directions: list[tuple[int, int]] = [DOWN, UP, RIGHT, LEFT]

directions_names = ["UP", "DOWN", "LEFT", "RIGHT"]

# COORDS
X = 1
Y = 0