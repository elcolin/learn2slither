from snake import Snake
from map import Map
from display import DisplayGame
import signal
from simulation import Simulation
from game_state import GameState
from param import Parameters

SUCCESS = True
FAILURE = False
NUMBER_OF_ACTIONS = 4


def main():
    param = Parameters()
    game_state = GameState(
        Snake([(1, 1), (1, 2), (1, 3)]), Map(param.map_size_))
    display: DisplayGame = DisplayGame(param.map_size_, param.display_)
    simulation: Simulation = Simulation(game_state, display, param)
    signal.signal(signal.SIGINT, simulation.ctrl_c_save_model)
    display.root.mainloop()


if __name__ == "__main__":
    main()
