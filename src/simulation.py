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
        self.initial_game_state_ = initial_game_state
        self.display_ = display
        if (param.learn_ == True):
            self.q = Q(1)
        else:
            self.q = Q(0)
        if (param.source_file_ is not None):
            self.q.load_q_table(param.q_table_)
        self.sessions_idx_ = 0
        self.reset_simulation()

    def reset_simulation(self):
        game_state  = GameState(Snake([(1,1), (1,2), (1,3)]), Map(self.param.map_size_))
        game_state.map_.generate_apples(NUMBER_OF_GREEN_APPLE, GREEN_APPLE)
        game_state.map_.generate_apples(NUMBER_OF_RED_APPLE, RED_APPLE)
        self.display_.set_timer_callback(self.param.timer_ms_, lambda : self.simulate(game_state))

    def simulate(self, game_state: GameState):
        print("---")
        if (self.param.sessions_ != -1 and self.sessions_idx_ >= self.param.sessions_ ):
            self.save_model()
        self.display_.draw_grid(game_state.map_.grid_)

        # st = game_state.map_.get_snake_surroundings(game_state.snake_.head_, self.param.depth_)
        st = []
        at = []
        qt = []
        action: Optional[int] = 0
        for i in range(len(directions)):
            st.append(game_state.map_.get_direction(directions[i], game_state.snake_.head_, self.param.depth_))
            if (st[i] not in self.q.q_table_):
                print("out")
                self.q.create_state(st[i])
                # print(st[i])
                at.append(self.q.generate_action(st[i], 1))
                qt.append(self.q.get_qt_max(st[i]))
            else:
                at.append(self.q.generate_action(st[i], 0.1))
                qt.append(self.q.get_qt_max(st[i]))
            print(st[i])
        # print("at: ", at)
        # print("qt: ", qt)
        i = np.argmax(qt)
        new_coord = game_state.snake_.project_head(directions[i])
        print("new_coord: ", new_coord)
        item = game_state.map_.grid_[new_coord]

        game_state.game_iteration(i, item)
        # new_st = game_state.map_.get_snake_surroundings(game_state.snake_.head_, self.param.depth_)
        new_st = []
        new_qt = []
        for k in range(len(directions)):
            new_st.append(game_state.map_.get_direction(directions[k], game_state.snake_.head_, self.param.depth_))
            if (new_st[k] not in self.q.q_table_):
                self.q.create_state(new_st[k])
                new_qt.append(self.q.get_qt_max(st[k]))
            else:
                new_qt.append(self.q.get_qt_max(new_st[k]))
        # print(new_st[k])
        j = np.argmax(new_qt)
        r = self.q.evaluate_item(item)

        print("r:", r, "qt:", qt[i], "at:", at[i], "new_qt:", new_qt[j])
        self.q.update(r, st[i], at[i], new_st[j])
        if not game_state.is_snake_alive():
            self.reset_simulation()
            return
        self.display_.draw_grid(game_state.map_.grid_)
        self.display_.update_snake(len(game_state.snake_.snake_coords_))
        print("len", len(game_state.snake_.snake_coords_))
        self.display_.set_timer_callback(self.param.timer_ms_, lambda : self.simulate(game_state))

    def ctrl_c_save_model(self, signum, frame):
        self.save_model()
        
    def save_model(self):
        if self.param.destination_file_ is None:
            sys.exit(0)
        #print("\nSauvegarde de la Q-table...")
        np.save(self.param.destination_file_, self.q.q_table_)
        #print("Sauvegarde terminée !")
        sys.exit(0)
