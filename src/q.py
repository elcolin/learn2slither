import numpy as np
from utils import *
import copy

LEARNING_RATE = 0.1
class Q :
    def __init__(self, learning_rate : np.float64):
        self.learning_rate_: np.float64 = learning_rate
        self.discount_factor_: np.float64 = 0.9 #gamma
        self.r : np.float64 = 0
        # self.eps : np.float64  = 0.1
        self.q_table_ = {}
        # self.q_table_['0000'] = [[0.0, 0.0, 0.0, 0.0]]

    def load_q_table(self, q_table: dict):
        self.q_table = q_table
    def create_state(self, key):
        if (key not in self.q_table_):
            self.q_table_[key] = [0.0, 0.0, 0.0, 0.0]
    def generate_action(self, st, eps: np.float64) -> int:
        if (random.uniform(0, 1) < eps):
            randomint = random.randint(0, 3)
            return randomint
        argmax = np.argmax(self.q_table_[st])
        return argmax

    def update(self, r: np.float64, st, at: int, st1):
        max_q_value_st1 = np.max(self.q_table_[st1])
        q_value_at_st = self.q_table_[st][at]
        self.q_table_[st][at] = (1 - self.learning_rate_) * q_value_at_st  + self.learning_rate_ * (r + self.discount_factor_ * max_q_value_st1)

    def evaluate_item(self, item: str) -> np.float64:
        v = str(item)
        r : int = 0
        match v:
            case 'W': r = -10
            case '0': r = -0.2
            case 'R': r = -1
            case 'S': r = -10
            case 'G': r = 1
            case _: r = 0
        return r
    def print(self):
        print(self.q_table_)
        