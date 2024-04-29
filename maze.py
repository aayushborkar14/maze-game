import random
import time

import numpy as np


class Maze:
    """
    Class to generate a maze using different algorithms

    self.cells: np.array, the maze
    """

    def __init__(self, level, side=70):
        """
        Initialize the maze object
        Args:
            level: int/str, The level of the maze to be generated
            side: The side length of the maze (default 70)
        Level 1: Growing Tree algorithm
        Level 2: Prim's algorithm
        Level 3: Wilson's algorithm
        Level "cave": Recursive Backtracking
        """
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
            self.growing_tree()
        elif level == 2:
            self.prim()
        elif level == 3:
            self.wilson()
        elif level == "cave":
            self.recursive_backtrack()
            self.recurse_sol()

    def check_bounds(self, x, y):
        """
        Check if the given coordinates are within the maze bounds
        Args:
            x: int, x-coordinate
            y: int, y-coordinate
        Returns:
            bool, True if within bounds, False otherwise
        """
        return 0 <= x < self.side and 0 <= y < self.side

    def num_to_coords(self, num):
        """
        Convert a number to coordinates in the maze
        Args:
            num: int, the number to be converted
        Returns:
            tuple, the coordinates
        """
        n = self.side // 2 + 1
        return 2 * (num % n), 2 * (num // n)

    def kruskal(self):
        """
        Generate a maze using the Kruskal's algorithm
        """
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
        # solve the maze and write the path
        self.solution = self.solve_maze(
            [[False for _ in range(self.side)] for _ in range(self.side)]
        )
        self.write_path()

    def prim(self):
        """
        Generate a maze using the Prim's algorithm
        """
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
        # solve the maze and write the path
        self.solution = self.solve_maze(
            [[False for _ in range(self.side)] for _ in range(self.side)]
        )
        self.write_path()

    def growing_tree(self):
        """
        Generate a maze using the Growing Tree algorithm
        This algorithm is a generalization of the Recursive Backtracking algorithm
        My implementation picks the last added cell with a probability of 70% and a random cell with 30%
        """
        for x in range(self.side):
            for y in range(self.side):
                if not (x % 2 == 1 and y % 2 == 1):
                    self.cells[x, y] = False
        x, y = (
            2 * random.randint(0, self.side // 2),
            2 * random.randint(0, self.side // 2),
        )
        cells = []
        cells.append((x, y))
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        visited = [[False for _ in range(self.side)] for _ in range(self.side)]
        visited[x][y] = True
        while cells:
            a = random.randint(1, 100)
            if a <= 70:
                # pick the most recent cell from the list
                x, y = cells[-1]
            else:
                # pick a random cell from the list
                x, y = random.choice(cells)
            found_one = False
            random.shuffle(dirs)
            for dx, dy in dirs:
                nx, ny = x + 2 * dx, y + 2 * dy
                if self.check_bounds(nx, ny) and not visited[nx][ny]:
                    found_one = True
                    visited[nx][ny] = True
                    self.parent[x + dx, y + dy] = (x, y)
                    self.parent[nx, ny] = (x + dx, y + dy)
                    if dx == 0:
                        if self.check_bounds(nx + 1, ny):
                            self.cells[nx + 1, ny] = True
                        if self.check_bounds(nx - 1, ny):
                            self.cells[nx - 1, ny] = True
                    elif dy == 0:
                        if self.check_bounds(nx, ny + 1):
                            self.cells[nx, ny + 1] = True
                        if self.check_bounds(nx, ny - 1):
                            self.cells[nx, ny - 1] = True
                    self.cells[x + dx, y + dy] = False
                    cells.append((nx, ny))
            if not found_one:
                cells.remove((x, y))
        # solve the maze and write the path
        self.solution = self.solve_maze(
            [[False for _ in range(self.side)] for _ in range(self.side)]
        )
        self.write_path()

    def solve_maze(self, visited, x=0, y=0):
        """
        Solve the maze using recursive DFS
        """
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
        """
        Generate a maze using the recursive backtracking algorithm
        """
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
        """
        Solve the maze if it is recursive backtracking
        """
        u = (self.side - 1, self.side - 1)
        while u:
            self.solution.append(u)
            self.sol_cells[u] = False
            u = self.parent[u]
        self.write_path()

    def write_path(self):
        """
        Write the path string consisting of L, R, U, D to a file
        File name is path.txt for levels 1, 2, 3 or cave_path.txt for cave level
        """
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
        """
        Generate a maze using the Wilson's algorithm
        """
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
        # solve the maze and write the path
        self.solution = self.solve_maze(
            [[False for _ in range(self.side)] for _ in range(self.side)]
        )
        self.write_path()


class DisjointSet:
    """
    Disjoint set data structure.
    """

    def __init__(self, n):
        """
        Initialize the data structure.
        Args:
            n: int, the number of elements.
        Returns:
            DisjointSet, the data structure object
        """
        self.parent = [0 for _ in range(n)]
        self.rank = [0 for _ in range(n)]

    def make_set(self, v):
        """
        Make a set with a single element.
        Args:
            v: int, the element.
        """
        self.parent[v] = v
        self.rank[v] = 0

    def find_set(self, v):
        """
        Find the representative of the set containing the element.
        Args:
            v: int, the element whose set representative is to be found.
        Returns:
            int, the representative of the set containing the element.
        """
        if v == self.parent[v]:
            return v
        self.parent[v] = self.find_set(self.parent[v])
        return self.parent[v]

    def union_sets(self, a, b):
        """
        Take the union of the sets containing the elements.
        Args:
            a: int, the first element.
            b: int, the second element.
        """
        a = self.find_set(a)
        b = self.find_set(b)
        if a != b:
            if self.rank[a] < self.rank[b]:
                a, b = b, a
            self.parent[b] = a
            if self.rank[a] == self.rank[b]:
                self.rank[a] += 1
