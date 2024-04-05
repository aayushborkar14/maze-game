import random
import time
import numpy as np
from disjoint_set import DisjointSet


class Maze:
    def __init__(self, level=1, side=70):
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
        if level == 1:
            self.recursive_backtrack()
            self.recurse_sol()
        elif level == 2:
            self.kruskal()
        elif level == 3:
            self.wilson()

    def check_bounds(self, x, y):
        return 0 <= x < self.side and 0 <= y < self.side

    def num_to_coords(self, num):
        n = self.side // 2 + 1
        return 2 * (num % n), 2 * (num // n)

    def kruskal(self):
        n = self.side // 2 + 1
        dsu = DisjointSet(n**2)
        for i in range(n**2):
            dsu.make_set(i)
        edge_list = []
        for a in range(n**2):
            x, y = self.num_to_coords(a)
            if x < self.side - 2:
                edge_list.append((a, a + 1))
            if y < self.side - 2:
                edge_list.append((a, a + n))
        random.shuffle(edge_list)
        for a, b in edge_list:
            if dsu.find_set(a) == dsu.find_set(b):
                continue
            dsu.union_sets(a, b)
            x1, y1 = self.num_to_coords(a)
            x2, y2 = self.num_to_coords(b)
            if x1 == x2:
                self.cells[x1, (y1 + y2) // 2] = False
                self.cells[x1, y1] = False
                self.cells[x1, y2] = False
            elif y1 == y2:
                self.cells[(x1 + x2) // 2, y1] = False
                self.cells[x1, y1] = False
                self.cells[x2, y1] = False
        self.solution = self.solve_maze(
            [[False for _x in range(self.side)] for _y in range(self.side)]
        )
        self.write_path()

    def solve_maze(self, visited, x=0, y=0):
        if visited[x][y]:
            return False
        visited[x][y] = True
        if x == self.side - 1 and y == self.side - 1:
            return [(x, y)]
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if not self.check_bounds(nx, ny):
                continue
            if self.cells[nx, ny]:
                continue
            a = self.solve_maze(visited, nx, ny)
            if a:
                a.append((x, y))
                return a
        return False

    def recursive_backtrack(self, x=0, y=0):
        self.cells[x, y] = False
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        random.shuffle(dirs)
        for dx, dy in dirs[::-1]:
            nx, ny = x + 2 * dx, y + 2 * dy
            if self.check_bounds(nx, ny) and self.cells[nx, ny]:
                self.cells[x + dx, y + dy] = False
                self.parent[(x + dx, y + dy)] = (x, y)
                self.parent[(nx, ny)] = (x + dx, y + dy)
                self.recursive_backtrack(nx, ny)
        return

    def recurse_sol(self):
        u = (self.side - 1, self.side - 1)
        while u:
            self.solution.append(u)
            self.sol_cells[*u] = False
            u = self.parent[u]
        self.write_path()

    def write_path(self):
        prex, prey = 0, 0
        pathstr = ""
        for y, x in self.solution[::-1]:
            self.sol_cells[y, x] = False
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

    def wilson(self):
        unvisited = [
            (x, y) for x in range(0, self.side, 2) for y in range(0, self.side, 2)
        ]
        first = random.choice(unvisited)
        unvisited.remove(first)
        self.cells[first] = False
        pres_path = []
        while unvisited:
            first = random.choice(unvisited)
            pres = first
            pres_path = [first]
            erase = False
            while True:
                dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
                dx, dy = random.choice(dirs)
                nx, ny = pres[0] + 2 * dx, pres[1] + 2 * dy
                tries = 0
                while (
                    (not self.check_bounds(nx, ny)) or ((nx, ny) in pres_path)
                ) and tries < 6:
                    dx, dy = random.choice(dirs)
                    nx, ny = pres[0] + 2 * dx, pres[1] + 2 * dy
                    tries += 1
                if not self.check_bounds(nx, ny):
                    erase = True
                    break
                if (nx, ny) in pres_path:
                    erase = True
                    break
                if (nx, ny) in unvisited:
                    pres_path.append((pres[0] + dx, pres[1] + dy))
                    pres_path.append((nx, ny))
                    pres = (nx, ny)
                else:
                    pres_path.append((pres[0] + dx, pres[1] + dy))
                    break
            if not erase:
                for u in pres_path:
                    self.cells[u] = False
                    if u in unvisited:
                        unvisited.remove(u)
        self.solution = self.solve_maze(
            [[False for _x in range(self.side)] for _y in range(self.side)]
        )
        self.write_path()
