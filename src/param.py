import argparse
import numpy as np
from typing import Optional

TIMER_MS = 1
MAP_SIZE = 10


class Parameters:
    def __init__(self):
        parser = argparse.ArgumentParser(description="")
        parser.add_argument(
            "--no-display",   # nom de l'argument
            action="store_false",
            help="Disable display"
        )
        parser.add_argument(
            "--src",
            type=str,
            help="Use source model (npy)"
        )
        parser.add_argument(
            "--dst",
            type=str,
            help="Stores destination file model (npy)"
        )
        parser.add_argument(
            "--timer",
            type=int,
            help="Time between each loop in milliseconds"
        )
        parser.add_argument(
            "--sessions",
            type=int,
            help="Number of training sessions"
        )
        parser.add_argument(
            "--map-size",
            type=int,
            help="Number of cells on the map"
        )
        parser.add_argument(
            "--no-learn",
            action="store_true",
            help="No q values updated"
        )
        parser.add_argument(
            "--walls",
            action="store_true",
            help="Spawns random walls"
        )
        args = parser.parse_args()
        self.map_size_ = MAP_SIZE
        if args.map_size is not None:
            self.map_size_ = args.map_size  # add map size argument
        self.walls_ = args.walls
        self.display_ = args.no_display
        self.timer_ms_ = TIMER_MS
        if (args.timer is not None):
            self.timer_ms_ = args.timer
        self.sessions_: int = -1
        if (args.sessions is not None):
            self.sessions_ = args.sessions
        if (args.src is not None):
            try:
                self.q_table_ = np.load("models/" + args.src, allow_pickle=True).item()
            except BaseException:
                print(
                    "Loading q table failed,\
                    does the file exist and in correct format ?")
                exit()
        self.destination_file_: Optional[str] = args.dst
        self.source_file_: Optional[str] = args.src
        self.no_learn_ = args.no_learn  # float ?
