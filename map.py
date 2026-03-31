from utils import *

class Map:
    def __init__(self, size: int):
        self.map_size_ : int = size
        self.grid_ : str = np.full((size, size), EMPTY)
        self.green_apples_coords_ : list[tuple[int]] = []
        self.red_apples_coords_ : list[tuple[int]] = []
        self.generate_mandatory_walls()
        self.generate_random_walls(10)
        self.generate_green_apples(3)
        self.generate_red_apples(3)

    def is_empty_space(self, coord: tuple[int]) -> bool:
        if (self.grid_[coord] == EMPTY):
            return True
        return False

    def evaluate_value(self, coord: tuple[int]) -> int:
        match self.grid_[coord]:
            case 'W' | 'S':
                return -2
            case 'R':
                return -1
            case 'G':
                return 1
            case '0':
                return 0
                
    def generate_coords(self) -> tuple[int]:
        return (generate_random(1, self.map_size_ - 2), generate_random(1, self.map_size_ - 2))

    def generate_valid_coords(self) -> tuple[int]:
        coords: tuple[int] = (0, 0)
        while (not self.is_empty_space(coords)) :
            coords = self.generate_coords()
        return coords
    
    def generate_red_apples(self, number_of_apples: int):
        for _ in range(number_of_apples):
            coords : tuple[int] = self.generate_valid_coords()
            self.red_apples_coords_.append(coords)
            self.grid_[coords] = RED_APPLE
            
    def generate_green_apples(self, number_of_apples: int):
        for _ in range(number_of_apples):
            coords : tuple[int] = self.generate_valid_coords()
            self.green_apples_coords_.append(coords)
            self.grid_[coords] = GREEN_APPLE

    def generate_random_walls(self, number_of_walls: int):
        for _ in range(number_of_walls):
            self.grid_[self.generate_valid_coords()] = WALL

    def generate_mandatory_walls(self):
        self.grid_[0, :] = WALL
        self.grid_[:, 0] = WALL
        self.grid_[-1, :] = WALL
        self.grid_[:, -1] = WALL

    def print(self):
        print(self.grid_)