import random
import time
import numpy as np


class Maze:
    def __init__(self, side=70):
        self.side = side - int(side % 2 == 0)
        self.cells = np.full(
            (self.side, self.side), True
        )  # True if wall, False if path
        self.parent = {}
        self.parent[(0, 0)] = None
        self.solution = []
        self.sol_cells = np.full(
            (self.side, self.side), True
        )  # True if wall, False if path
        random.seed(time.time())
        self.gen_maze()
        self.gen_sol()

    def check_bounds(self, x, y):
        return 0 <= x < self.side and 0 <= y < self.side

    def gen_maze(self, x=0, y=0):
        self.cells[x, y] = False
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        random.shuffle(dirs)
        while len(dirs):
            dx, dy = dirs.pop()
            nx = x + 2 * dx
            ny = y + 2 * dy
            if self.check_bounds(nx, ny) and self.cells[nx][ny]:
                self.cells[x + dx, y + dy] = False
                self.parent[(x + dx, y + dy)] = (x, y)
                self.parent[(nx, ny)] = (x + dx, y + dy)
                self.gen_maze(nx, ny)
        return

    def gen_sol(self):
        u = (self.side - 1, self.side - 1)
        while u:
            self.solution.append(u)
            self.sol_cells[*u] = False
            u = self.parent[u]
        prex, prey = 0, 0
        pathstr = ""
        for y, x in self.solution[::-1]:
            if x == 0 and y == 0:
                continue
            if x == prex:
                if y > prey:
                    pathstr += "D"
                else:
                    pathstr += "U"
            elif y == prey:
                if x > prex:
                    pathstr += "R"
                else:
                    pathstr += "L"
            prex, prey = x, y
        with open("path.txt", "w+") as f:
            f.write(pathstr)

    def __str__(self):
        string = ""
        conv = {True: "██", False: "  "}
        for x in range(self.side):
            for y in range(self.side):
                string += conv[self.sol_cells[x, y]]
            string += "\n"
        return string
