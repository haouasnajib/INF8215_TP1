import copy

from Graph import Graph


class Solution(object):
    def __init__(self, s):
        if isinstance(s, Graph):
            self.g = s
            self.cost = 0
            self.visited = []
            self.not_visited = []
            for i in range(s.N):
                self.not_visited.append(i)
        elif isinstance(s, Solution):
            self.g = copy.copy(s.g)
            self.cost = copy.copy(s.cost)
            self.visited = copy.copy(s.visited)
            self.not_visited = copy.copy(s.not_visited)
        else:
            raise ValueError('you should give a graph or a solution')

    def add_edge(self, v, u):
        self.visited.append(u)
        self.not_visited.remove(u)
        self.cost = self.cost + self.g.costs[u, v]

    def print(self):
        print(self.visited[len(self.visited)-1], end='')
        for i in self.visited:
            print(' >', i, end='')
        print('\nCoût :', self.cost)