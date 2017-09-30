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
        smallest_connected_edge = None  # This edge connects the partial solution to the nearest city

        # Attempt
        for e_edge in all_sorted_edges:
            if (e_edge.source == source or e_edge.destination == source) and (e_edge.source in sol.not_visited and e_edge.destination in sol.not_visited):
                self.uf.add(e_edge)
                mst_cost += e_edge.cost
                break

        for s_edge in all_sorted_edges:
            if not sol.visited:
                if s_edge.source == source or s_edge.destination == source:  # No need to check if other end is in not_visited: it is, all cities are there
                    smallest_connected_edge = s_edge
                    break  # We could just break here because everything is sorted, we found the smallest edge that starts or ends at source
            else:
                if (s_edge.source == sol.visited[len(sol.visited) - 1] and s_edge.destination in sol.not_visited and s_edge.source != source and s_edge.destination != source) or \
                        (s_edge.destination == sol.visited[len(sol.visited) - 1] and s_edge.source in sol.not_visited and s_edge.source != source and s_edge.destination != source):
                    smallest_connected_edge = s_edge
                    break  # We could just break here because everything is sorted, we found the smallest edge that starts or ends at source

        for i_edge in all_sorted_edges:
            if (i_edge.source in sol.not_visited) and (i_edge.destination in sol.not_visited) and i_edge.source != source and i_edge.destination != source:
                useful_sorted_edges.append(i_edge)  # At the very start, no other edge originating from city_start is considered but smallest_connected_edge previously set

        if smallest_connected_edge is not None:  # It is possible at this point that not_visited is empty, meaning nothing has been assigned to smallest_connected_edge, hence this check
            # is it admissible? Yes, while this is no longer an MST, this is slightly larger than an MST.
            # The complete solution contains at least one of such edges (connected ones to the current source that is),
            # not the shortest one especially. And what comes after is at least of cost equal to MST. This means our
            # heuristic will always at most be equal to the solution's remaining cost.
            self.uf.add(smallest_connected_edge)
            mst_cost += smallest_connected_edge.cost

        for e_edge in useful_sorted_edges:
            if not self.uf.makes_cycle(e_edge):
                self.uf.add(e_edge)
                mst_cost += e_edge.cost

        return mst_cost
