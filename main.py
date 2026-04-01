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

    def game_iteration(self, at: int) -> tuple[tuple[int, int], str]:
        st = self.snake_.take_action(at)
        item: str = self.map_.grid_[st]
        print(item)
        self.update_game(st)
        return st, item
        
DEPTH = 100
TIMER_MS = 10
class Simulation:

    def __init__(self, initial_game_state: GameState, display: DisplayGame):
        self.initial_game_state_ = initial_game_state
        self.display_ = display
        self.q = Q(MAP_SIZE * MAP_SIZE, NUMBER_OF_ACTIONS)
        self.reset_simulation()

    def reset_simulation(self):
        game_state = copy.deepcopy(self.initial_game_state_)
        self.display_.set_timer_callback(TIMER_MS, lambda : self.simulate(game_state, 0))

    def simulate(self, game_state: GameState, idx: int):
        self.display_.draw_grid(game_state.map_.grid_)

        init_coord = game_state.snake_.head_
        init_st = self.q.get_row(init_coord)

        at = self.q.generate_action(init_st)
        # while (
        #         game_state.snake_.project_head(directions[at])[X] < 0 or
        #         game_state.snake_.project_head(directions[at])[X] >= MAP_SIZE or
        #         game_state.snake_.project_head(directions[at])[Y] < 0 or
        #         game_state.snake_.project_head(directions[at])[Y] >= MAP_SIZE
        # ):
        #     # print(at)
        #     at = self.q.generate_action(init_st)
        new_coord = game_state.snake_.project_head(directions[at])
        item = game_state.map_.grid_[new_coord]
        # new_coord, item = game_state.game_iteration(at)

        new_st = self.q.get_row(new_coord)
        new_q_value = self.q.q_table_[new_st, np.argmax(self.q.q_table_[new_st])]

        r = self.q.evaluate_item(item, idx)
        print(f"r: {r}")
        self.q.q_table_[init_st, at] += (r + self.q.discount_factor_ * (new_q_value - self.q.q_table_[init_st, at]))
        # print(f"{at} {new_st} {directions_names[at]} {directions_names[at]}")
        if idx > DEPTH or item == 'W':
            self.reset_simulation()
            return
        idx += 1
        game_state.game_iteration(at)
        # self.q.print()
        self.display_.draw_grid(game_state.map_.grid_)
        self.display_.set_timer_callback(TIMER_MS, lambda : self.simulate(game_state, idx))

def main():
    parser = argparse.ArgumentParser(description="") 
    parser.add_argument(
    "--display",   # nom de l'argument
    action="store_true",  # si présent, devient True
    help="Activer l'affichage"
)
    args = parser.parse_args()
    signal.signal(signal.SIGINT, handle_ctrl_c)
    game_state = GameState(Snake([(1,1), (1,2), (1,3)]), Map(MAP_SIZE))
    display : DisplayGame = DisplayGame(args.display)
    simulation : Simulation = Simulation(game_state, display)
    display.root.mainloop()

if __name__ == "__main__":
    main()