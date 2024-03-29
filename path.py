import random
import time
from queue import PriorityQueue


class Path:
    def __init__(self, side):
        random.seed(time.time())
        self.side = side + int(side % 2 == 0)
        self.path = []
        self.cells = [[True for _y in range(self.side)] for _x in range(self.side)]
        self.generate_path()

    def check_bounds(self, pos):
        return (0 <= pos[0] < self.side) and (0 <= pos[1] < self.side)

    def generate_path(self, start=(1, 1), end=None):
        if end is None:
            end = (self.side - 2, self.side - 2)
        open_q = PriorityQueue()
        open_q.put((0, start))
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        source_dict = {start: None}
        while not open_q.empty():
            _, u = open_q.get()
            endfound = False
            for d in dirs:
                v = (u[0] + d[0] * 2, u[1] + d[1] * 2)
                vi = (u[0] + d[0], u[1] + d[1])
                if self.check_bounds(v) and v not in source_dict:
                    source_dict[v] = vi
                    source_dict[vi] = u
                    if v == end:
                        endfound = True
                        break
                    open_q.put((-random.randint(0, self.side**2), v))
            if endfound:
                break
        v = end
        while v is not None:
            self.cells[v[0]][v[1]] = False
            self.path.append(v)
            v = source_dict[v]

    def __str__(self):
        string = ""
        conv = {True: "██", False: "  "}
        for x in range(self.side):
            for y in range(self.side):
                string += conv[self.cells[x][y]]
            string += "\n"
        return string
