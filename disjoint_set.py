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
