import random
import time

import numpy as np

from disjoint_set import DisjointSet


class Maze:
    def __init__(self, level, side=70):
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
        self.level = level
        random.seed(time.time())
        if level == 1:
            # self.recursive_backtrack()
            # self.recurse_sol()
            self.eller()
        elif level == 2:
            self.prim()
        elif level == 3:
            self.wilson()
        elif level == "cave":
            self.recursive_backtrack()
            self.recurse_sol()

    def check_bounds(self, x, y):
        return 0 <= x < self.side and 0 <= y < self.side

    def num_to_coords(self, num):
        n = self.side // 2 + 1
        return 2 * (num % n), 2 * (num // n)

    def eller(self):
        self.cells = np.vstack([self.cells, np.full((1, self.side), True)])
        # consider even rows only
        weight_lists = [False] * 60 + [True] * 40
        prev_sets = []
        for i in range(0, self.side, 2):
            sets = []
            if i:
                sets = prev_sets
                not_in_set = []
                for j in range(0, self.side, 2):
                    self.cells[i, j] = self.cells[i - 2, j]
                    self.cells[i + 1, j] = self.cells[i - 1, j]
                    if j + 1 < self.side:
                        self.cells[i, j + 1] = False
                    if self.cells[i + 1, j]:
                        for idx, s in enumerate(sets):
                            if j in s:
                                break
                        if sets[idx] == {j}:
                            sets.pop(idx)
                        else:
                            sets[idx].remove(j)
                        not_in_set.append(j)
                    self.cells[i + 1, j] = False
                for j in not_in_set:
                    sets.append({j})
                sets.sort(key=min)
                set_idx = 0
                for j in range(0, self.side - 2, 2):
                    for set_idx, s in enumerate(sets):
                        if j in s:
                            break
                    if j + 2 in sets[set_idx]:
                        self.cells[i, j + 1] = True
                    elif random.choice(weight_lists):
                        self.cells[i, j + 1] = True
                    else:
                        j2_idx = 0
                        for j2_idx, j2 in enumerate(sets):
                            if j + 2 in j2:
                                break
                        sets[set_idx] = sets[set_idx].union(sets[j2_idx])
                        sets.pop(j2_idx)
            else:
                for j in range(0, self.side, 2):
                    if j == 0 or self.cells[i, j - 1]:
                        sets.append({j})
                    else:
                        sets[-1].add(j)
                    self.cells[i, j] = False
                    if j + 1 < self.side:
                        self.cells[i, j + 1] = random.choice(weight_lists)
            for j in range(0, self.side, 2):
                self.cells[i + 1, j] = True
            if i + 1 < self.side:
                for s in sets:
                    sl = list(s)
                    for _ in range(random.randint(1, len(s) // 2 + 1)):
                        sj = random.choice(sl)
                        self.cells[i + 1, sj] = False
                        sl.remove(sj)
            prev_sets = sets
        # last row processing
        for s in prev_sets:
            if max(s) + 1 < self.side:
                self.cells[self.side - 1, max(s) + 1] = False
        self.cells = self.cells[: self.side, :]

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
            [[False for _ in range(self.side)] for _ in range(self.side)]
        )
        self.write_path()

    def prim(self):
        n = self.side // 2 + 1
        x, y = 2 * random.randint(0, n - 1), 2 * random.randint(0, n - 1)
        path = [(x, y)]
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        walls = []
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if self.check_bounds(nx, ny):
                walls.append((nx, ny))
        for x in range(n):
            for y in range(n):
                self.cells[2 * x, 2 * y] = False
        while walls:
            wx, wy = random.choice(walls)
            unvisited = ()
            if wx % 2 == 0:
                if (wx, wy - 1) in path and (wx, wy + 1) not in path:
                    unvisited = (wx, wy + 1)
                elif (wx, wy + 1) in path and (wx, wy - 1) not in path:
                    unvisited = (wx, wy - 1)
            else:
                if (wx - 1, wy) in path and (wx + 1, wy) not in path:
                    unvisited = (wx + 1, wy)
                elif (wx + 1, wy) in path and (wx - 1, wy) not in path:
                    unvisited = (wx - 1, wy)
            if unvisited:
                self.cells[wx, wy] = False
                path.append(unvisited)
                for dx, dy in dirs:
                    nx, ny = unvisited[0] + dx, unvisited[1] + dy
                    if self.check_bounds(nx, ny):
                        walls.append((nx, ny))
            walls.remove((wx, wy))
        self.solution = self.solve_maze(
            [[False for _ in range(self.side)] for _ in range(self.side)]
        )
        self.write_path()

    def solve_maze(self, visited, x=0, y=0):
        if visited[x][y]:
            return []
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
        return []

    def recursive_backtrack(self, x=0, y=0):
        self.cells[x, y] = False
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        random.shuffle(dirs)
        for dx, dy in dirs:
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
        pathfilename = "path.txt"
        if self.level == "cave":
            pathfilename = "cave_path.txt"
        with open(pathfilename, "w+") as f:
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
            [[False for _ in range(self.side)] for _ in range(self.side)]
        )
        self.write_path()
