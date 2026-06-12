import numpy as np
import random
from utils import MAP_SIZE


class Q:

    """
        Class used to generate a Q Table
            States are keys following the given format:
                ('0', '0', 'W')
                Note : tuple size can vary
            States access to Q values in the Q table:
                [0.0, 0.0, 0.0, 0.0]
                These values represent the reward from each action
                (UP, DOWN, RIGHT, LEFT)

    """

    def __init__(self, learning_rate: np.float64):
        self.learning_rate_: np.float64 = learning_rate
        self.discount_factor_: np.float64 = 0.9  # gamma
        self.q_table_ = {}
        self.empt_ = 0

    def get_q_table_size(self):
        return len(self.q_table_)

    def load_q_table(self, q_table: dict):
        self.q_table_ = q_table

    def create_state(self, st: tuple[str]):
        """
            Creates a q spacing for q values of a given state
                Args:
                    st: state, the given key
        """
        if (st not in self.q_table_):
            self.q_table_[st] = [0.0, 0.0, 0.0, 0.0]

    def get_qt_max(self, st: tuple[str]):
        """
            Gets best Q value based on state
            Args:
                st: Represents a key used to index Q values
        """
        return np.max(self.q_table_[st])

    def generate_action(self, st, eps: np.float64) -> int:
        if (random.uniform(0, 1) < eps):
            randomint = random.randint(0, 3)
            return randomint
        # print(self.q_table_[st])
        argmax = np.argmax(self.q_table_[st])
        return argmax

    def update(self, r: np.float64, st, at: int, st1):
        """ Updates the q value of the state based
        on the reward of the new state and best outcome
            Args:
                r : reward
                st : state
                st1 : new state
                at : the index of the wanted q value (index of action)
        """
        max_q_value_st1 = np.max(self.q_table_[st1])
        q_value_at_st = self.q_table_[st][at]

        self.q_table_[st][at] = (
            1 - self.learning_rate_) * q_value_at_st + self.learning_rate_ * (
            r + self.discount_factor_ * max_q_value_st1)

    def evaluate_item(self, item: str) -> np.float64:
        v = str(item)

        r: int = 0
        if (item != '0'):
            self.empt_ = 0
        match v:
            case 'W': r = -2
            case '0':
                r = max(-0.5, (-0.1 / MAP_SIZE) * self.empt_)
                self.empt_ = self.empt_ + 1
            case 'R': r = -1
            case 'S': r = -2
            case 'G': r = 1
            case _: r = 0
        return r

    def print(self):
        print(self.q_table_)
