from display import DisplayGame
from q import Q
from game_state import GameState
from param import Parameters
from snake import Snake
from utils import directions
from map import Map
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
        self.display_.set_timer_callback(self.param.timer_ms_, lambda : self.simulate(game_state))

    def simulate(self, game_state: GameState):
        if (self.param.sessions_ != -1 and self.sessions_idx_ >= self.param.sessions_ ):
            self.save_model()
        self.sessions_idx_ += 1
        self.display_.draw_grid(game_state.map_.grid_)

        # st = game_state.map_.get_snake_surroundings(game_state.snake_.head_, self.param.depth_)
        st = []
        at = []
        qt = []
        for i in range(len(directions)):
            st.append(game_state.map_.get_direction(game_state.snake_.head_, directions[i], self.param.depth_))
            if (st[i] not in self.q.q_table_):
                self.q.create_state(st[i])
                at.append(self.q.generate_action(st[i], 1))
                qt.append(self.q.get_qt_max(st[i]))
            else:
                at.append(self.q.generate_action(st[i], 0.1))
                qt.append(self.q.get_qt_max(st[i]))
        print(st)
        print(at)
        print(qt)
        i = np.argmax(qt)
        # if (st not in self.q.q_table_):
        #     self.q.create_state(st)
        #     at = self.q.generate_action(st, 1)
        # else:
        #     at = self.q.generate_action(st, 0.1)
        new_coord = game_state.snake_.project_head(directions[at[i]])
        item = game_state.map_.grid_[new_coord]
        game_state.game_iteration(at[i], item)
        # new_st = game_state.map_.get_snake_surroundings(game_state.snake_.head_, self.param.depth_)
        new_st = []
        new_qt = []
        for k in range(len(directions)):
            new_st.append(game_state.map_.get_direction(game_state.snake_.head_, directions[k], self.param.depth_))
            if (new_st[k] not in self.q.q_table_):
                self.q.create_state(new_st[k])
                new_qt.append(self.q.get_qt_max(st[k]))
            else:
                new_qt.append(self.q.get_qt_max(new_st[k]))
        j = np.argmax(new_qt)
        r = self.q.evaluate_item(item)
        self.q.update(r, st[i], at[i], new_st[j])
        if not game_state.is_snake_alive():
            self.reset_simulation()
            return
        self.display_.draw_grid(game_state.map_.grid_)
        self.display_.set_timer_callback(self.param.timer_ms_, lambda : self.simulate(game_state))

    def ctrl_c_save_model(self, signum, frame):
        self.save_model()
        
    def save_model(self):
        if self.param.destination_file_ is None:
            sys.exit(0)
        print("\nSauvegarde de la Q-table...")
        np.save(self.param.destination_file_, self.q.q_table_)
        print("Sauvegarde terminée !")
        sys.exit(0)
