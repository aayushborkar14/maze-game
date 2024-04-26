import numpy as np


class PowerUp:
    """
    Ennumerate the powerups as integers.
    """

    EMPTY = 1
    SCORE_GAIN = 2
    TIME_GAIN = 3
    CAVE_VENT = 4


class PowerUpMap:
    """
    Generates a powerup map for a given side length and powerup weights.
    Places powerups randomly on pillar cells.

    self.map: np.array, the powerup map.
    """

    def __init__(self, side, weights):
        """
        Initialize the powerup map.
        Args:
            side: int, the side length of the map.
            weights: dict, the weights of the powerups.
        """
        self.side = side - int(side % 2 == 0)
        self.map = np.zeros((side, side), dtype=int)
        power_ups = list(weights.keys())
        power_weights = list(weights.values())
        for i in range(1, self.side, 2):
            for j in range(1, self.side, 2):
                self.map[i, j] = np.random.choice(power_ups, p=power_weights)
