from utils import X, Y, directions

SNAKE_IS_DEAD = 0
SNAKE_IS_ALIVE = 1


class Snake:
    def __init__(self, snake_coords: list[tuple]):
        self.snake_coords_: list[tuple] = []
        self.head_: tuple[int, int] = []
        self.body_: list[tuple] = []
        self.tampered_coords_: tuple[int, int] = []
        self._init_snake_position(snake_coords)

    def project_head(self, direction: tuple[int, int]) -> tuple[int]:
        return (self.head_[Y] + direction[Y], self.head_[X] + direction[X])

    def take_action(self, at_idx: tuple[int]) -> tuple[int, int]:
        # self.update_snake(self.project_head(direction))
        # print(directions[action])
        new_head_coords = self.project_head(directions[at_idx])
        # print(new_head_coords)
        self.head_to_tail(self.head_)
        self.define_new_head_coords(new_head_coords)
        return new_head_coords

    def add_tail(self):
        self.body_.append(self.tampered_coords_)
        self.snake_coords_.append(self.tampered_coords_)
        self.tampered_coords_ = []

    def head_to_tail(self, old_head_coords: tuple[int, int]):
        self.body_.insert(0, old_head_coords)

    def delete_tail(self):
        if self.body_:
            self.tampered_coords_ = self.body_[-1]
            self.body_.pop()
        self.snake_coords_.pop()
        if not self.snake_coords_:
            return SNAKE_IS_DEAD
        return SNAKE_IS_ALIVE

    def define_new_head_coords(self, head_coords: tuple[int]):
        self.snake_coords_.insert(0, head_coords)
        self.head_ = head_coords

    def _init_snake_position(self, coords: list[tuple]):
        self.snake_coords_ = coords
        self.head_ = coords[0]
        self.body_ = coords[1:]
