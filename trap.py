import numpy as np


class Trap:
    EMPTY = 1
    SPRITE_FREEZE = 2
    TIME_LOSS = 3
    SCORE_LOSS = 4
    START_AGAIN = 5
    REDUCED_VISION = 6


class TrapMap:
    def __init__(self, maze, weights):
        self.map = np.zeros(maze.shape, dtype=int)
        weight_keys = list(weights.keys())
        weight_values = list(weights.values())
        for i in range(maze.shape[0]):
            for j in range(maze.shape[1]):
                if self.map[i, j] != 0:
                    continue
                self.map[i, j] = Trap.EMPTY
                if all(
                    [
                        (0 <= i + k < maze.shape[0]) and maze[i + k, j] == 0
                        for k in range(-2, 3)
                    ]
                ):
                    skipthis = False
                    if j - 1 >= 0 and maze[i, j - 1] == 0:
                        skipthis = True
                    if j + 1 < maze.shape[1] and maze[i, j + 1] == 0:
                        skipthis = True
                    if not skipthis:
                        for k in range(-2, 3):
                            self.map[i + k, j] = Trap.EMPTY
                        self.map[i, j] = np.random.choice(weight_keys, p=weight_values)
                if all(
                    [
                        (0 <= j + k < maze.shape[1]) and maze[i, j + k] == 0
                        for k in range(-2, 3)
                    ]
                ):
                    skipthis = False
                    if i - 1 >= 0 and maze[i - 1, j] == 0:
                        skipthis = True
                    if i + 1 < maze.shape[0] and maze[i + 1, j] == 0:
                        skipthis = True
                    if not skipthis:
                        for k in range(-2, 3):
                            self.map[i, j + k] = Trap.EMPTY
                        self.map[i, j] = np.random.choice(weight_keys, p=weight_values)
