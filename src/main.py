from snake import Snake
from map import Map
from display import DisplayGame
import signal
from simulation import Simulation
from param import Parameters

SUCCESS = True
FAILURE = False
NUMBER_OF_ACTIONS = 4


def main():
    param = Parameters()
    display: DisplayGame = DisplayGame(param.map_size_, param.display_)
    simulation: Simulation = Simulation(display, param)
    signal.signal(signal.SIGINT, simulation.ctrl_c_save_model)
    display.root.mainloop()


if __name__ == "__main__":
    main()
