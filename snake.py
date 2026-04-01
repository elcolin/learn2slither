from utils import *

class Snake :
    def __init__(self, snake_coords: list[tuple]):
        self.snake_coords_ : list[tuple] = []
        self.head_ : tuple[int, int] = []
        self.body_ : list[tuple] = []
        self.tampered_coords_ : tuple[int, int] = []
        self._init_snake_position(snake_coords)

    def project_head(self, direction: tuple[int, int]) -> tuple[int]:
        return (self.head_[Y] + direction[Y], self.head_[X] + direction[X])
    
    def take_action(self, action: tuple[int]) -> tuple[int, int]:
        # self.update_snake(self.project_head(direction))
        new_head_coords = self.project_head(directions[action])
        print(self.head_)
        print(new_head_coords)
        self.head_to_tail(self.head_)
        self.define_new_head_coords(new_head_coords)
        self.delete_tail()
        return new_head_coords

    def head_to_tail(self, old_head_coords: tuple[int, int]):
        self.body_.insert(0, old_head_coords)

    def delete_tail(self):
        if not self.snake_coords_:
            return
        self.tampered_coords_ = self.body_[-1]
        self.snake_coords_.pop()
        self.body_.pop()

    def define_new_head_coords(self, head_coords: tuple[int]):
        # print(head_coords)
        self.snake_coords_.insert(0, head_coords)
        self.head_ = head_coords
        
    # def move_snake(self, head_coords: tuple[int]):
        # if self.snake_coords_ :
            # self.tampered_coords_ = self.body_[-1]
            # self.snake_coords_.pop()
            # self.snake_coords_.insert(0, head_coords)
            # self.body_.pop()
            # self.body_.insert(0, self.head_)
        # self.head_ = head_coords

    def _init_snake_position(self, coords: list[tuple]):
        self.snake_coords_ = coords
        self.head_ = coords[0]
        self.body_ = coords[1:]