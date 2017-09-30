import numpy as np

kruskal = None


class UnionFind(object):
    def __init__(self, n):
        self.n = n
        self.parent = np.array(range(n))
        self.rnk = np.zeros(n)

    def reset(self):
        self.parent = np.array(range(self.n))
        self.rnk = np.zeros(self.n)

    def add(self, e):
        x = self.find(e.source)
        y = self.find(e.destination)

        if self.rnk[x] > self.rnk[y]:
            self.parent[y] = x
        else:
            self.parent[x] = y
        if self.rnk[x] == self.rnk[y]:
            self.rnk[y] += 1

    def makes_cycle(self, e):
        return self.find(e.source) == self.find(e.destination)

    def find(self, u):
        if u != self.parent[u]:
            return self.find(self.parent[u])
        else:
            return u


class Kruskal(object):
    def __init__(self, g):
        self.uf = UnionFind(g.N)
        self.g = g

    def getMSTCost(self, sol, source):
        mst_cost = 0
        self.uf.reset()

        all_sorted_edges = self.g.get_sorted_edges()
        useful_sorted_edges = []

        if not sol.visited:
            useful_sorted_edges = all_sorted_edges
        else:
            for i_edge in all_sorted_edges:
                if i_edge.source in sol.not_visited and i_edge.destination in sol.not_visited:
                    useful_sorted_edges.append(i_edge)
                elif (i_edge.source == sol.visited[len(sol.visited)-1] and i_edge.destination in sol.not_visited) or \
                        (i_edge.destination == sol.visited[len(sol.visited)-1] and i_edge.source in sol.not_visited):
                    useful_sorted_edges.append(i_edge)

        for e_edge in useful_sorted_edges:
            if not self.uf.makes_cycle(e_edge):
                self.uf.add(e_edge)
                mst_cost += e_edge.cost

        return mst_cost
