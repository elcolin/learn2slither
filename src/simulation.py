from display import DisplayGame
from q import Q
from game_state import GameState
from param import Parameters
from snake import Snake
from utils import directions, X, Y
from map import Map, NUMBER_OF_GREEN_APPLE, NUMBER_OF_RED_APPLE, RED_APPLE, GREEN_APPLE, MAP_SIZE
from typing import Optional
import numpy as np
import sys
from collections import defaultdict


class Simulation:
    def __init__(self, initial_game_state: GameState, display: DisplayGame, param: Parameters):
        self.param = param
        self.display_ = display
        if (param.no_learn_ == True):
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
        if (self.param.sessions_ != -1 and self.sessions_idx_ >= self.param.sessions_ ):
            self.exit()
        self.sessions_idx_ += 1
        game_state  = GameState(Snake([(1,1), (1,2), (1,3)]), Map(self.param.map_size_))
        game_state.map_.generate_apples(NUMBER_OF_GREEN_APPLE, GREEN_APPLE)
        game_state.map_.generate_apples(NUMBER_OF_RED_APPLE, RED_APPLE)
        self.display_.set_timer_callback(self.param.timer_ms_, lambda : self.simulate(game_state))


    def simulate(self, game_state: GameState):
        print("---")
        game_state.map_.print_snakes_vision(game_state.snake_.head_)
        st = []
        at = []
        qt = []

        for i in range(len(directions)):
        # "random rate": chooses random action 10 percent of the time
            eps : int = 0.1
            # Getting state in all directions
            fut_st = game_state.map_.get_direction(directions[i], game_state.snake_.head_)
            if fut_st in st:
                # If states exists more than once in current position than generate random
                eps = 1
                idx = st.index(fut_st)
                at[idx] = self.q.generate_action(st[idx], eps)
            st.append(fut_st)
            if (st[i] not in self.q.q_table_):
                self.q.create_state(st[i])
                # If state doesn't exist, then go fully random on action choice
                eps = 1
            at.append(self.q.generate_action(st[i], eps))
            qt.append(self.q.q_table_[st[i]][at[i]])

        # Getting idx for the highest q value
        at_idx = np.argmax(qt)
        new_coord = game_state.snake_.project_head(directions[at_idx])
        item = game_state.map_.grid_[new_coord]

        game_state.game_iteration(at_idx, item)

        new_st = []
        new_qt = []

        for k in range(len(directions)):
            new_st.append(game_state.map_.get_direction(directions[k], game_state.snake_.head_))
            if (new_st[k] not in self.q.q_table_):
                self.q.create_state(new_st[k])
                # Appending max Q value to new state based on previous state
            new_qt.append(self.q.get_qt_max(new_st[k]))

        new_at_idx = np.argmax(new_qt)
        r = self.q.evaluate_item(item)
        self.q.update(r, st[at_idx], at[at_idx], new_st[new_at_idx])


        self.display_.draw_grid(game_state.map_.grid_)
        snake_len = len(game_state.snake_.snake_coords_)
        self.best_ = snake_len if snake_len > self.best_ else self.best_
        self.update_display_stats(snake_len)

        if not game_state.is_snake_alive():
            self.tot_ += snake_len
            self.reset_simulation()
            self.death_wall_ = self.death_wall_ + 1 if item == 'W' else self.death_wall_
            self.death_snake_ = self.death_snake_ + 1 if item == 'S' else self.death_snake_
            game_state.map_.print_snakes_vision(game_state.snake_.head_)

            return

        self.display_.set_timer_callback(self.param.timer_ms_, lambda : self.simulate(game_state))


    def update_display_stats(self, snake_len: int):
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
        #print("\nSauvegarde de la Q-table...")
        np.save(self.param.destination_file_, self.q.q_table_)
        #print("Sauvegarde terminée !")
        sys.exit(0)
