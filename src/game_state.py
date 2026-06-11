from utils import RED_APPLE, GREEN_APPLE
from snake import SNAKE_IS_ALIVE, SNAKE_IS_DEAD, Snake
from map import Map


class GameState:
    def __init__(self, snake: Snake, map: Map):
        self.map_ = map
        self.snake_ = snake
        self.map_.update_snake_position(snake)
        self.snake_status_: int = SNAKE_IS_ALIVE

    def is_snake_alive(self) -> bool:
        if (self.snake_status_ == SNAKE_IS_ALIVE):
            return True
        return False

    def game_iteration(self, at_idx: int, item: str):
        """
            Updates map status and snake depending on the item
        """
        if (item == RED_APPLE):
            self.snake_status_ = self.snake_.delete_tail()
            self.map_.update_snake_position(self.snake_)
        self.snake_.take_action(at_idx)
        if (item != GREEN_APPLE):
            self.snake_status_ = self.snake_.delete_tail()
        if item == 'W' or item == 'S':
            self.snake_status_ = SNAKE_IS_DEAD
        self.map_.update_snake_position(self.snake_)
