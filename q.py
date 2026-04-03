import numpy as np
from utils import *


class Q :
    def __init__(self, number_of_states: int, number_of_actions: int, learning_rate : np.float64):
        self.learning_rate_: np.float64 = learning_rate
        self.discount_factor_: np.float64 = 0.9 #gamma
        self.number_of_states_ = number_of_states
        self.number_of_actions_ = number_of_actions
        self.r : np.float64 = 0
        # self.eps : np.float64  = 0.1
        self.q_table_['0000'] = {[0.0, 0.0, 0.0, 0.0]}

    def create_state(self, key):
        if (key not in self.q_table_):
            self.q_table_[key] = {[0.0, 0.0, 0.0, 0.0]}
    def get_row(self, coord: tuple[int, int]) -> int:
        row : int = coord[Y] * (MAP_SIZE - 1) + coord[X]
        return row

    def generate_action(self, st: int, eps: np.float64) -> int:
        if (random.uniform(0, 1) < eps):
            randomint = generate_random_int(0, 3)
            return randomint
        argmax = np.argmax(self.q_table_[st])
        return argmax

    def update(self, r: np.float64, st: int, at: int, st1: int):
        max_q_value_st1 = np.max(self.q_table_[st1])
        q_value_at_st = self.q_table_[st, at]
        self.q_table_[st, at] = (1 - self.learning_rate_) * q_value_at_st  + self.learning_rate_ * (r + self.discount_factor_ * max_q_value_st1)

    def evaluate_item(self, item: str, t: int) -> np.float64:
        v = str(item)
        r : int = 0
        match v:
            case 'W': r = -1
            case '0': r = -0.2
            case 'R': r = -1
            case 'S': r = -10
            case 'G': r = 1
            case _: r = 0
        return r
    def print(self):
        print(self.q_table_)
        