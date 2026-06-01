from utils import *
from snake import *
import copy
class Map:
    def __init__(self, size: int):
        self.map_size_ : int = size
        self.grid_ : str = np.full((size, size), EMPTY)
        self.green_apples_coords_ : list[tuple[int]] = []
        self.red_apples_coords_ : list[tuple[int]] = []
        self.generate_mandatory_walls()
        # self.generate_random_int_walls(MAP_SIZE)
        self.copy_grid_ = copy.deepcopy(self.grid_)
        # self.generate_apples(NUMBER_OF_GREEN_APPLE, GREEN_APPLE)
        # self.generate_apples(NUMBER_OF_RED_APPLE, RED_APPLE)

    def is_empty_space(self, coord: tuple[int]) -> bool:
        if (self.grid_[coord] == EMPTY):
            return True
        return False
    def return_item(self, coords: tuple[int, int]) -> str:
        return self.grid_[coords]
    
    def project_coord(self, head_coords:tuple[int, int], add_coords: tuple[int, int]):
        new_y = head_coords[Y] + add_coords[Y]
        new_x = head_coords[X] + add_coords[X]
        
        # limiter dans la grille
        new_y = max(0, min(new_y, len(self.grid_) - 1))
        new_x = max(0, min(new_x, len(self.grid_[0]) - 1))
        return (new_y, new_x)

    def get_snakes_vision(self, head_coords: tuple[int, int]):
        key: str = []
        for y in range(self.grid_.shape[Y]) :
            if y == head_coords[Y]:
                for char in self.grid_[y]:
                    key += str(self.grid_[y])
                continue
            for x in range(self.grid_.shape[1]):
                if x == head_coords[X]:
                    key += str(self.grid_[y][x])
                    continue
        return key
    def return_key_vision(self, head_coords: tuple[int, int]) -> str:
        key: str = self.get_snakes_vision(head_coords)
        self.print_snakes_vision(head_coords)
        # for direction in directions:
        # 
            # coords = self.project_coord(head_coords, direction)
            # if (self.grid_[coords] == SNAKE_HEAD):
                # key += EMPTY
                # continue
            # key += self.grid_[self.project_coord(head_coords, direction)]
        # key += self.grid_[self.project_coord(head_coords, RIGHT)]
        # key += self.grid_[self.project_coord(head_coords, LEFT)]

        # key += self.grid_[head_coords[Y] + DOWN[Y], head_coords[X] + DOWN[X]]
        # key += self.grid_[head_coords[Y] + RIGHT[Y], head_coords[X] + RIGHT[X]]
        # key += self.grid_[head_coords[Y] + LEFT[Y], head_coords[X] + LEFT[X]]
        key = tuple(key)
        return key
    
    def print_snakes_vision(self, head_coords: tuple[int, int]):
        for y in range(self.grid_.shape[Y]) :
            if y == head_coords[Y]:
                for char in self.grid_[y]:
                    print(char, end='')
                print()
                continue
            for x in range(self.grid_.shape[1]):
                if x == head_coords[X]:
                    print(self.grid_[y][x], end='')
                    continue
                print(' ', end='')
            print()
        
    def update_snake_position(self, snake: Snake) :
        if snake.tampered_coords_ is not None:
            self.grid_[snake.tampered_coords_] = self.copy_grid_[snake.tampered_coords_]
        for coord in snake.body_:
            self.grid_[coord] = SNAKE_BODY
        if (self.grid_[snake.head_] == GREEN_APPLE):
            self.generate_apples(1, GREEN_APPLE)
        if (self.grid_[snake.head_] == RED_APPLE):
            self.generate_apples(1, RED_APPLE)
        self.grid_[snake.head_] = SNAKE_HEAD
                
    def generate_coords(self) -> tuple[int]:
        return (generate_random_int(1, self.map_size_ - 2), generate_random_int(1, self.map_size_ - 2))

    def generate_valid_coords(self) -> tuple[int]:
        coords: tuple[int] = (0, 0)
        while (not self.is_empty_space(coords)) :
            coords = self.generate_coords()
        return coords
    
    def generate_apples(self, number_of_apples: int, apple_type: str):
        for _ in range(number_of_apples):
            coords : tuple[int] = self.generate_valid_coords()
            self.red_apples_coords_.append(coords)
            self.grid_[coords] = apple_type

    def generate_random_int_walls(self, number_of_walls: int):
        for _ in range(number_of_walls):
            self.grid_[self.generate_valid_coords()] = WALL

    def generate_mandatory_walls(self):
        self.grid_[0, :] = WALL
        self.grid_[:, 0] = WALL
        self.grid_[-1, :] = WALL
        self.grid_[:, -1] = WALL

    def print(self):
        print(self.grid_)