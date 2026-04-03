from snake import *
from map import *
from display import *
import tkinter as tk
import signal
import copy
import time
import argparse
from q import *

SUCCESS = True
FAILURE = False
NUMBER_OF_ACTIONS = 4

class GameState:
    def __init__(self, snake: Snake, map: Map):
        self.map_ = map
        self.snake_ = snake
        self.map_.update_snake_position(snake)
        
    def update_game(self, new_head_coords: tuple[int, int]):
        """
            Updates the state of the game
            Parameters: 
                New snake head position.
        """
        self.map_.update_snake_position(self.snake_)
        # self.map_.print_snakes_vision(self.snake_.head_)

    def game_iteration(self, at: int, item: str):
        if (item == RED_APPLE):
            self.snake_.delete_tail()
            self.map_.update_snake_position(self.snake_)
        new_head_coords = self.snake_.take_action(at)
        if (item != GREEN_APPLE):
            self.snake_.delete_tail()
        self.update_game(new_head_coords)
        
TIMER_MS = 10
LEARNING_RATE = 0.1
class Simulation:

    def __init__(self, initial_game_state: GameState, display: DisplayGame, args):
        self.initial_game_state_ = initial_game_state
        self.display_ = display
        if (args.learn == True):
            self.q = Q(MAP_SIZE * MAP_SIZE, NUMBER_OF_ACTIONS, LEARNING_RATE)
        else:
            self.q = Q(MAP_SIZE * MAP_SIZE, NUMBER_OF_ACTIONS, 0)
        self.destination_file_ : str = args.dst
        if (args.src is not None):
            self.q.q_table_ = np.load(args.src, allow_pickle=True).item()
            print(self.q.q_table_)
            print("Q Table loaded!")
        self.timer_ms_ = TIMER_MS
        if (args.timer is not None):
            self.timer_ms_ = args.timer
        self.sessions_ : int = -1
        if (args.sessions is not None):
            self.sessions_ = args.sessions
        self.sessions_idx_ = 0
        self.reset_simulation()

    def reset_simulation(self):
        game_state = copy.deepcopy(self.initial_game_state_)
        self.display_.set_timer_callback(self.timer_ms_, lambda : self.simulate(game_state))

    def simulate(self, game_state: GameState):
        if (self.sessions_ != -1 and self.sessions_idx_ >= self.sessions_ ):
            self.save_model()
        self.sessions_idx_ += 1
        self.display_.draw_grid(game_state.map_.grid_)

        init_coord = game_state.snake_.head_
        # init_st = self.q.get_row(init_coord)

        st = game_state.map_.return_key_vision(init_coord)
        print()
        if (st not in self.q.q_table_):
            self.q.create_state(st)
            at = self.q.generate_action(st, 0)
        else:
            at = self.q.generate_action(st, 0)
        new_coord = game_state.snake_.project_head(directions[at])
        item = game_state.map_.grid_[new_coord]
        game_state.game_iteration(at, item)

        new_st = game_state.map_.return_key_vision(new_coord)
        if (new_st not in self.q.q_table_):
            self.q.create_state(new_st)
        r = self.q.evaluate_item(item)
        print(self.q.q_table_[new_st])
        self.q.update(r, st, at, new_st)
        if item == 'W' or item == 'S':
            self.reset_simulation()
            return
        self.display_.draw_grid(game_state.map_.grid_)
        self.display_.set_timer_callback(self.timer_ms_, lambda : self.simulate(game_state))

    def ctrl_c_save_model(self, signum, frame):
        self.save_model()
    def save_model(self):
        if self.destination_file_ is None:
            sys.exit(0)
        print("\nSauvegarde de la Q-table...")
        np.save(self.destination_file_, self.q.q_table_)
        print("Sauvegarde terminée !")
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="") 
    parser.add_argument(
    "--display",   # nom de l'argument
    action="store_true",  # si présent, devient True
    help="Activer l'affichage"
    )
    parser.add_argument(
    "--src",
    type=str
    )

    parser.add_argument(
    "--dst",
    type=str
    )

    parser.add_argument(
        "--timer",
        type=int
    )
    parser.add_argument(
        "--sessions",
        type=int        
    )

    parser.add_argument(
        "--learn",
        action="store_true"
    )

    parser.add_argument(
        "--no-random",
        action="store_false"
    )


    args = parser.parse_args()
    game_state = GameState(Snake([(1,1), (1,2), (1,3)]), Map(MAP_SIZE))
    display : DisplayGame = DisplayGame(args.display)
    simulation : Simulation = Simulation(game_state, display, args)
    signal.signal(signal.SIGINT, simulation.ctrl_c_save_model)
    display.root.mainloop()

if __name__ == "__main__":
    main()