from enum import IntEnum, unique, auto

import numpy as np


@unique
class PowerUp(IntEnum):
    EMPTY = auto()
    SCORE_GAIN = auto()
    TIME_GAIN = auto()
    SCORE_LOSS = auto()
    TIME_LOSS = auto()
    DUNGEON = auto()


class PowerUpMap:
    def __init__(self, side, weights):
        self.side = side - int(side % 2 == 0)
        self.map = np.zeros((side, side))
