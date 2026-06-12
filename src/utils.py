WALL = 'W'
SNAKE_HEAD = 'H'
SNAKE_BODY = 'S'
GREEN_APPLE = 'G'
RED_APPLE = 'R'
EMPTY = '0'

MAP_SIZE = 10
NUMBER_OF_GREEN_APPLE = 2
NUMBER_OF_RED_APPLE = 1

UP: tuple[int, int] = (-1, 0)
DOWN: tuple[int, int] = (1, 0)
LEFT: tuple[int, int] = (0, -1)
RIGHT: tuple[int, int] = (0, 1)

directions: list[tuple[int, int]] = [UP, RIGHT, DOWN, LEFT]
opposite_directions: list[tuple[int, int]] = [DOWN, LEFT, UP, RIGHT]


# opposite_directions: list[tuple[int, int]] = [DOWN, UP, RIGHT, LEFT]

direction_names = ["UP", "RIGHT", "DOWN", "LEFT"]
opposite_direction_names = ["DOWN", "LEFT", "UP", "RIGHT"]

# COORDS
X = 1
Y = 0
