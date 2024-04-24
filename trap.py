import numpy as np


class Trap:
    EMPTY = 1
    SPRITE_FREEZE = 2
    REDUCED_VISION = 3


class TrapMap:
    def __init__(self, maze, weights):
        self.map = np.zeros(maze.shape, dtype=int)
        weight_keys = list(weights.keys())
        weight_values = list(weights.values())
        for i in range(maze.shape[0]):
            for j in range(maze.shape[1]):
                if self.map[i, j] == Trap.EMPTY:
                    continue
                self.map[i, j] = Trap.EMPTY
                if any(
                    [
                        0 <= i + k < maze.shape[0]
                        and 0 <= j + k < maze.shape[1]
                        and maze[i + k, j + k] == 0
                        for k in (-1, 1)
                    ]
                ) or any(
                    [
                        0 <= i + k < maze.shape[0]
                        and 0 <= j - k < maze.shape[1]
                        and maze[i + k, j - k] == 0
                        for k in (-1, 1)
                    ]
                ):
                    self.map[i, j] = Trap.EMPTY
                    continue
                k = 0
                while True:
                    if i + k < maze.shape[0] and maze[i + k, j] == 0:
                        k += 1
                    else:
                        break
                if k >= 5:
                    for h in range(k):
                        self.map[i + h, j] = Trap.EMPTY
                    self.map[i + (k - 1) // 2, j] = np.random.choice(
                        weight_keys, p=weight_values
                    )
                k = 0
                while True:
                    if j + k < maze.shape[1] and maze[i, j + k] == 0:
                        k += 1
                    else:
                        break
                if k >= 5:
                    for h in range(k):
                        self.map[i, j + h] = Trap.EMPTY
                    self.map[i, j + (k - 1) // 2] = np.random.choice(
                        weight_keys, p=weight_values
                    )
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
