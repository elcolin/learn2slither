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
        help="Desactiver l'affichage"
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
            "--map-size",
            type=int
        )
        parser.add_argument(
            "--no-learn",
            action="store_true"
        )
        parser.add_argument(
            "--no-random",
            action="store_false"
        )
        args = parser.parse_args()
        self.map_size_ = MAP_SIZE
        if args.map_size is not None:
            self.map_size_ = args.map_size # add map size argument
        self.display_ = args.no_display
        self.timer_ms_ = TIMER_MS
        if (args.timer is not None):
            self.timer_ms_ = args.timer
        self.sessions_ : int = -1
        if (args.sessions is not None):
            self.sessions_ = args.sessions
        if (args.src is not None):
            try:
                self.q_table_ = np.load(args.src, allow_pickle=True).item()
            except:
                print("Loading q table failed, does the file exist and in correct format ?")
                exit()
        self.destination_file_ : Optional[str] = args.dst
        self.source_file_ : Optional[str] = args.src
        self.no_learn_ = args.no_learn # float ?

        