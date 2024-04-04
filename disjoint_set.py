class DisjointSet:
    def __init__(self, n):
        self.parent = [0 for _ in range(n)]
        self.rank = [0 for _ in range(n)]

    def make_set(self, v):
        self.parent[v] = v
        self.rank[v] = 0

    def find_set(self, v):
        if v == self.parent[v]:
            return v
        self.parent[v] = self.find_set(self.parent[v])
        return self.parent[v]

    def union_sets(self, a, b):
        a = self.find_set(a)
        b = self.find_set(b)
        if a != b:
            if self.rank[a] < self.rank[b]:
                a, b = b, a
            self.parent[b] = a
            if self.rank[a] == self.rank[b]:
                self.rank[a] += 1
