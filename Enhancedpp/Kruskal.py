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

        # Starting MST with smallest possible edge directly connected to source and having one vertex in not_visited
        for e_edge in all_sorted_edges:
            if (e_edge.source == source or e_edge.destination == source) and (e_edge.source in sol.not_visited and e_edge.destination in sol.not_visited):
                # Is our heuristic still admissible here? Yes, previously we had an estimate that was always less than
                # the remaining cost of the solution because we never complete a cycle to city_start. Here we add the
                # smallest possible edge that connects city_start with unvisited cities. This means that adding this to
                # our previous heuristic will only bring us ever so closer to the solution's true cost without going
                # over it since either that vertex is in the real solution and it's ok or it is not and there is a
                # bigger edge taking its place
                self.uf.add(e_edge)
                mst_cost += e_edge.cost
                break  # Edges are sorted, the first one found is the smallest

        # Selecting smallest_connected_edge out of all possible edges, this edge shares the last vertex from the
        # solution and one with not_visited. It is the same as e_edge above if the solution is empty. This doesn't
        # hurt our heuristic since this is still the smallest edge to be connected to source (which in the case of empty
        # solution is both the source and the current city)
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

        # Looking for all vertices that don't touch the solution
        for i_edge in all_sorted_edges:
            if (i_edge.source in sol.not_visited) and (i_edge.destination in sol.not_visited) and i_edge.source != source and i_edge.destination != source:
                useful_sorted_edges.append(i_edge)  # At the very start, no other edge originating from city_start is considered but smallest_connected_edge previously set

        # Continuing MST with smallest possible edge directly connected to solution
        if smallest_connected_edge is not None:  # It is possible at this point that not_visited is empty, meaning nothing has been assigned to smallest_connected_edge, hence this check
            # is it admissible? Yes, while this is no longer an MST, this is slightly larger than an MST.
            # The complete solution contains at least one of such edges (connected ones to the current source that is),
            # not the shortest one especially. And what comes after in the solution is of cost less than MST.
            # This is because we don't go back to city_start. This means our heuristic will always be less than the
            # solution's remaining cost at this point.
            self.uf.add(smallest_connected_edge)
            mst_cost += smallest_connected_edge.cost

        for e_edge in useful_sorted_edges:
            if not self.uf.makes_cycle(e_edge):
                self.uf.add(e_edge)
                mst_cost += e_edge.cost

        return mst_cost
