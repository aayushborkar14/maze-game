from enum import IntEnum, auto, unique

import numpy as np


@unique
class PowerUp(IntEnum):
    EMPTY = auto()
    SCORE_GAIN = auto()
    TIME_GAIN = auto()
    JUMP = auto()
    SCORE_LOSS = auto()
    TIME_LOSS = auto()
    CAVE_VENT = auto()


class PowerUpMap:
    def __init__(self, side, weights):
        self.side = side - int(side % 2 == 0)
        self.map = np.zeros((side, side), dtype=int)
        power_ups = weights.keys()
        power_weights = weights.values()
        for i in range(1, self.side, 2):
            for j in range(1, self.side, 2):
                self.map[i][j] = np.random.choice(
                    list(power_ups), p=list(power_weights)
                )
