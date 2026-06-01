import argparse
import numpy as np
from typing import Optional

TIMER_MS = 1
MAP_SIZE = 10

class Parameters:
    def __init__(self):
        parser = argparse.ArgumentParser(description="") 
        parser.add_argument(
        "--no_display",   # nom de l'argument
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
            "--learn",
            action="store_true"
        )
        parser.add_argument(
            "--no-random",
            action="store_false"
        )
        parser.add_argument(
            "--depth",
            type=int)
        args = parser.parse_args()
        self.map_size_ = MAP_SIZE # add map size argument
        self.display_ = args.no_display
        self.timer_ms_ = TIMER_MS
        if (args.timer is not None):
            self.timer_ms_ = args.timer
        self.sessions_ : int = -1
        if (args.sessions is not None):
            self.sessions_ = args.sessions
        if (args.src is not None):
            self.q_table_ = np.load(args.src, allow_pickle=True).item()
        self.destination_file_ : Optional[str] = args.dst
        self.source_file_ : Optional[str] = args.src
        self.learn_ = args.learn # float ?
        self.depth_ = args.depth

        