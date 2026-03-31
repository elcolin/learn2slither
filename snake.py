from utils import *

class Snake :
    def __init__(self, snake_coords: list[tuple], grid: np.array):
        self.snake_coords_ : list[tuple] = []
        self.snake_head_ : tuple = []
        self.snake_body_ : list[tuple] = []
        self._init_snake_position(snake_coords)
        self._update_snake_display(grid)

    def project_head(self, direction: tuple[int, int]) -> tuple[int]:
        return (self.snake_head_[Y] + direction[Y], self.snake_head_[X] + direction[X])
    def action(self, direction: tuple[int], grid: np.array):
        self.update_snake(self.project_head(direction), grid)

    def update_snake(self, head_coords: tuple[int], grid: np.array):
        if self.snake_coords_ :
            grid[self.snake_coords_[-1]] = EMPTY
            self.snake_coords_.pop()
            self.snake_coords_.insert(0, head_coords)
            self.snake_body_.pop()
            self.snake_body_.insert(0, self.snake_head_)
        self.snake_head_ = head_coords
        self._update_snake_display(grid)

    def _init_snake_position(self, coords: list[tuple]):
        self.snake_coords_ = coords
        self.snake_head_ = coords[0]
        self.snake_body_ = coords[1:]

    def _update_snake_display(self, grid: np.array):
        grid[self.snake_head_] = SNAKE_HEAD
        for coord in self.snake_body_:
            grid[coord] = SNAKE_BODY

    def print(self, grid: np.array):
        print(grid[self.snake_head_[Y]])
        print(grid[:, self.snake_head_[X]])