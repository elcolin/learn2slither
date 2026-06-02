from display import DisplayGame
from q import Q
from game_state import GameState
from param import Parameters
from snake import Snake
from utils import directions
from map import Map, NUMBER_OF_GREEN_APPLE, NUMBER_OF_RED_APPLE, RED_APPLE, GREEN_APPLE
from typing import Optional
import numpy as np
import sys

class Simulation:
    def __init__(self, initial_game_state: GameState, display: DisplayGame, param: Parameters):
        self.param = param
        self.display_ = display
        if (param.learn_ == True):
            self.q = Q(1)
        else:
            self.q = Q(0)
        if (param.source_file_ is not None):
            self.q.load_q_table(param.q_table_)
        self.sessions_idx_ = 0
        self.tot_ = 0
        self.best_ = 0
        self.avg_coord_ = np.array([])
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
        # "random rate": chooses random action 10 percent of the time
        eps : int = 0.1

        for i in range(len(directions)):
            # Getting state in all directions
            st.append(game_state.map_.get_direction(directions[i], game_state.snake_.head_))
            if (st[i] not in self.q.q_table_):
                self.q.create_state(st[i])
                # If state doesn't exist, then go fully random on action choice
                eps = 1
            at.append(self.q.generate_action(st[i], eps))
            qt.append(self.q.get_qt_max(st[i]))

        # Getting idx for the highest q value
        at_idx = np.argmax(qt)
        new_coord = game_state.snake_.project_head(directions[at_idx])
        item = game_state.map_.grid_[new_coord]
        # test = np.std(self.avg_coord_, axis=1)
        # print(test)

        # print(st)
        # Execute action
        game_state.game_iteration(at_idx, item)
        self.avg_coord_.append(new_coord)

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
        if (snake_len > self.best_):
            self.best_ = len(game_state.snake_.snake_coords_)
        self.update_display_stats(snake_len)

        if not game_state.is_snake_alive():
            self.tot_ += snake_len
            self.reset_simulation()
            return

        self.display_.set_timer_callback(self.param.timer_ms_, lambda : self.simulate(game_state))


    def update_display_stats(self, snake_len: int):
        self.display_.update_snake(snake_len)
        self.display_.update_sessions(self.sessions_idx_)
        self.display_.update_avg(self.tot_ / self.sessions_idx_)
        self.display_.update_best(self.best_)

    def print_stats(self):
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
