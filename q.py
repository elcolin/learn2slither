import numpy as np
from utils import *
class Q :
    def __init__(self, number_of_states: int, number_of_actions: int):
        self.learning_rate_: np.float64 = 0.01
        self.discount_factor_: np.float64 = 0.9
        self.number_of_states_ = number_of_states
        self.number_of_actions_ = number_of_actions
        self.r : np.float64 = 0
        self.eps : np.float64  = 0.1
        self.q_table_ = np.zeros((number_of_states, number_of_actions))

    def generate_action(self, state: tuple[int, int]) -> int:
        if (random.uniform(0, 1) < self.eps):
            return generate_random_int(0, 3)
        return np.argmax(self.q_table_[state])

    def evaluate_item(self, item: str) -> np.float64:
        v = str(item)
        match v:
            case 'W': return -1
            case '0': return -0.1
            case 'R': return -1
            case 'S': return -1
            case 'G': return 1
            case _: return 0
    def print(self):
        print(self.q_table_)
        