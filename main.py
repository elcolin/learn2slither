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
MAP_SIZE = 10
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
        self.snake_.update_snake(new_head_coords)
        self.map_.update_snake_position(self.snake_)
        self.map_.print_snakes_vision(self.snake_.head_)

    # def state_projection(self, action: int) -> tuple[int, int]:
    #     coords = self.snake_.project_head(directions[action])
    #     return coords
    
    def game_iteration(self, action: int) -> tuple[tuple[int, int], str]:
        state : tuple[int, int] = self.snake_.project_head(directions[action])
        item: str = self.map_.grid_[state]
        self.update_game(state)
        return state, item
        
DEPTH = 20

class Simulation:
    def __init__(self, initial_game_state: GameState, display: DisplayGame):
        self.initial_game_state_ = initial_game_state
        self.display_ = display
        self.q = Q(MAP_SIZE * MAP_SIZE, NUMBER_OF_ACTIONS)
        self.reset_simulation()

    def reset_simulation(self):
        game_state = copy.deepcopy(self.initial_game_state_)
        self.display_.set_callback(lambda : self.simulate(game_state, 0))

    def simulate(self, game_state: GameState, idx: int):
        self.display_.draw_grid(game_state.map_.grid_)
        head = game_state.snake_.head_
        head_current_idx = head[Y] * (MAP_SIZE - 1) + head[X]
        action = self.q.generate_action(head_current_idx)
        state, item = game_state.game_iteration(action)
        r = self.q.evaluate_item(item)
        q_idx = state[Y] * (MAP_SIZE - 1) + state[X]
        self.q.q_table_[q_idx, action] += r 
        # self.q.print()
        if idx > DEPTH or self.q.r  < -2: 
            self.reset_simulation()
            return
        idx += 1
        self.display_.draw_grid(game_state.map_.grid_)
        self.display_.set_callback(lambda : self.simulate(game_state, idx))

def main():
    parser = argparse.ArgumentParser(description="") 
    parser.add_argument(
    "--display",   # nom de l'argument
    action="store_true",  # si présent, devient True
    help="Activer l'affichage"
)
    args = parser.parse_args()
    signal.signal(signal.SIGINT, handle_ctrl_c)
    game_state = GameState(Snake([(1,3), (1,4), (1,5)]), Map(10))
    display : DisplayGame = DisplayGame(args.display)
    simulation : Simulation = Simulation(game_state, display)
    display.root.mainloop()

if __name__ == "__main__":
    main()