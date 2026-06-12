from display import DisplayGame
from q import Q
from game_state import GameState
from param import Parameters
import utils as ut
from map import Map
import numpy as np
import sys


class Simulation:
    def __init__(
            self,
            display: DisplayGame,
            param: Parameters):
        self.param = param
        self.display_ = display
        if (param.no_learn_):
            self.q = Q(0)
        else:
            self.q = Q(1)
        if (param.source_file_ is not None):
            self.q.load_q_table(param.q_table_)
        self.sessions_idx_ = 0
        self.tot_ = 0
        self.best_ = 0
        self.death_wall_ = 0
        self.death_snake_ = 0
        self.reset_simulation()

    def reset_simulation(self):
        if (self.param.sessions_ != -
                1 and self.sessions_idx_ >= self.param.sessions_):
            self.exit()
        self.sessions_idx_ += 1
        game_state = GameState(
            Map(
                self.param.map_size_,
                self.param.walls_))
        game_state.map_.generate_apples(
            ut.NUMBER_OF_GREEN_APPLE,
            ut.GREEN_APPLE)
        game_state.map_.generate_apples(ut.NUMBER_OF_RED_APPLE, ut.RED_APPLE)
        self.display_.set_timer_callback(
            self.param.timer_ms_,
            lambda: self.simulate(game_state))

    def get_state(self, game_state: GameState, direction):
        st = game_state.map_.get_direction(direction, game_state.snake_.head_)
        return st

    def update_table_with_new_state(
            self,
            game_state,
            r,
            chosen_st,
            prediction_at):
        new_st = []
        new_qt = []

        for k in range(len(ut.directions)):
            new_st.append(self.get_state(game_state, ut.directions[k]))
            if (new_st[k] not in self.q.q_table_):
                self.q.create_state(new_st[k])
            # Appending max Q value of new state
            new_qt.append(self.q.get_qt_max(new_st[k]))
        new_at = np.argmax(new_qt)

        # Updating the q value of the previous state based on new state
        self.q.update(r, chosen_st, prediction_at, new_st[new_at])

    def get_states_values_actions_all_direction(self, game_state):
        """
            Gets state in each direction, the potential future actions with the
            highest q values and their associated max q values.
        """
        st = []
        at_in_fut = []
        qt = []

        for i in range(len(ut.directions)):
            # "random rate": chooses potential q value at
            # random 10 percent of the time or
            # 100 when state doesn't exist,
            # or state exists in multiple directions
            eps = 0.1
            # Getting state in direction
            fut_st = self.get_state(game_state, ut.directions[i])
            if (fut_st not in self.q.q_table_):
                self.q.create_state(fut_st)
                eps = 1
            indices = [i for i, state in enumerate(st) if state == fut_st]
            for prev_idx in indices:
                # If states exists more than once in position than go random
                eps = 1
                at_in_fut[prev_idx] = self.q.generate_action(st[prev_idx], eps)
            st.append(fut_st)
            at_in_fut.append(self.q.generate_action(fut_st, eps))
            qt.append(self.q.q_table_[fut_st][at_in_fut[i]])
        return st, qt, at_in_fut

    def simulate(self, game_state: GameState):
        """
            The function that runs a course of movement and updates the game
        """

        game_state.map_.print_snakes_vision(game_state.snake_.head_)
        st, qt, at_in_fut = (
            self.get_states_values_actions_all_direction(game_state))
        # Selecting the action based on best q value
        at = np.argmax(qt)
        new_coord = game_state.snake_.project_head(ut.directions[at])
        item = game_state.map_.grid_[new_coord]

        game_state.game_iteration(at, game_state.map_.grid_[new_coord])

        self.update_table_with_new_state(
            game_state,
            self.q.evaluate_item(item),
            st[at],
            at_in_fut[at])

        self.display_.draw_grid(game_state.map_.grid_)
        snake_len = len(game_state.snake_.snake_coords_)
        self.update_display_stats(snake_len)

        if not game_state.is_snake_alive():
            self.update_dead_snake_stats(snake_len, item)
            return

        self.display_.set_timer_callback(
            self.param.timer_ms_,
            lambda: self.simulate(game_state))

    def update_dead_snake_stats(self, snake_len: int, item):
        self.tot_ += snake_len
        self.q.empt_ = 0
        self.reset_simulation()
        self.death_wall_ += item == 'W'
        self.death_snake_ += item == 'S'

    def update_display_stats(self, snake_len: int):
        self.best_ = snake_len if snake_len > self.best_ else self.best_
        self.display_.update_snake(snake_len)
        self.display_.update_sessions(self.sessions_idx_)
        self.display_.update_avg(self.tot_ / self.sessions_idx_)
        self.display_.update_best(self.best_)

    def print_stats(self):
        print("Death by body:", self.death_snake_)
        print("Death by wall:", self.death_wall_)
        print("Number of sessions: ", self.sessions_idx_)
        print("Best snake length: ", self.best_)
        print("Average length: ", self.tot_ / self.sessions_idx_)
        print("Number of stored states: ", self.q.get_q_table_size())

    def exit(self):
        self.print_stats()
        self.save_model()

    def ctrl_c_save_model(self, signum, frame):
        self.exit()

    def save_model(self):
        if self.param.destination_file_ is None:
            sys.exit(0)
        np.save("../models/" + self.param.destination_file_, self.q.q_table_)
        sys.exit(0)
