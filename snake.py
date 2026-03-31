from utils import *

class Snake :
    def __init__(self, snake_coords: list[tuple]):
        self.snake_coords_ : list[tuple] = []
        self.head_ : tuple = []
        self.snake_body_ : list[tuple] = []
        self.tampered_coords_ : tuple[int, int] = []
        self._init_snake_position(snake_coords)

    def project_head(self, direction: tuple[int, int]) -> tuple[int]:
        return (self.head_[Y] + direction[Y], self.head_[X] + direction[X])
    
    def action(self, direction: tuple[int], grid: np.array):
        self.update_snake(self.project_head(direction), grid)

    def update_snake(self, head_coords: tuple[int]):
        if self.snake_coords_ :
            self.tampered_coords_ = self.snake_body_[-1]
            self.snake_coords_.pop()
            self.snake_coords_.insert(0, head_coords)
            self.snake_body_.pop()
            self.snake_body_.insert(0, self.head_)
        self.head_ = head_coords

    def _init_snake_position(self, coords: list[tuple]):
        self.snake_coords_ = coords
        self.head_ = coords[0]
        self.snake_body_ = coords[1:]