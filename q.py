import numpy as np
from utils import *


class Q :
    def __init__(self, number_of_states: int, number_of_actions: int):
        self.learning_rate_: np.float64 = 0.1
        self.discount_factor_: np.float64 = 0.9 #gamma
        self.number_of_states_ = number_of_states
        self.number_of_actions_ = number_of_actions
        self.r : np.float64 = 0
        self.eps : np.float64  = 0.1
        self.q_table_ = np.zeros((number_of_states, number_of_actions))

    def get_row(self, coord: tuple[int, int]) -> int:
        row : int = coord[Y] * (MAP_SIZE - 1) + coord[X]
        return row

    def generate_action(self, st: int) -> int:
        if (random.uniform(0, 1) < self.eps):
            randomint = generate_random_int(0, 3)
            print(randomint)
            return randomint
        argmax = np.argmax(self.q_table_[st])
        print(f"argmax: {argmax} , {self.q_table_[st]}")
        return argmax
    


    def evaluate_item(self, item: str, t: int) -> np.float64:
        v = str(item)
        r : int = 0
        match v:
            case 'W': r = -10
            case '0': r = -0.01
            case 'R': r = -1
            case 'S': r = -10
            case 'G': r = 1
            case _: r = 0
        return r
    def print(self):
        print(self.q_table_)
        