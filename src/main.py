from snake import *
from map import *
from display import *
import signal
from simulation import *
from game_state import *
from param import *
SUCCESS = True
FAILURE = False
NUMBER_OF_ACTIONS = 4

def main():
    param = Parameters()
    game_state = GameState(Snake([(1,1), (1,2), (1,3)]), Map(MAP_SIZE))
    display : DisplayGame = DisplayGame(param.display_)
    simulation : Simulation = Simulation(game_state, display, param)
    signal.signal(signal.SIGINT, simulation.ctrl_c_save_model)
    display.root.mainloop()

if __name__ == "__main__":
    main()