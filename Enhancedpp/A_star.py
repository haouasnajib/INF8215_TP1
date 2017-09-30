from heapqueue.binary_heap import BinaryHeap
import queue as Q

from Graph import Graph
import Kruskal
from Solution import Solution

import time

city_start = 0


class Node(object):
    n_nodes_explored = 0
    n_nodes_created = 0

    def __init__(self, v, sol, heuristic_cost):
        self.v = v
        self.solution = sol
        self.heuristic_cost = heuristic_cost

    def __gt__(self, other):
        return isN2betterThanN1(self, other)

    def explore_node(self, heap):
        Node.n_nodes_explored += 1

        for i in self.solution.not_visited:
            if i != self.v and i != city_start:
                sol = Solution(self.solution)
                sol.add_edge(self.v, i)  # Careful, not_visited can become empty here, pay attention to this in getMSTCost

                krus = Kruskal.kruskal
                heur = krus.getMSTCost(sol, city_start)
                # heur = 0
                nod = Node(i, sol, heur)

                Node.n_nodes_created += 1
                heap.put(nod)
            elif len(self.solution.not_visited) == 1:  # ( and i == city_start) Unnecessary to check that i is city_start because city_start is last, ensured by the first if.
                sol = Solution(self.solution)
                sol.add_edge(self.v, i)

                krus = Kruskal.kruskal
                heur = krus.getMSTCost(sol, city_start)
                # heur = 0
                nod = Node(i, sol, heur)

                Node.n_nodes_created += 1
                heap.put(nod)


def main():
    time_start = time.time()
    data_file = "N12.data"

    g = Graph(data_file)

    import Kruskal
    Kruskal.kruskal = Kruskal.Kruskal(g)
    krus = Kruskal.kruskal

    solution_start = Solution(g)

    heur = krus.getMSTCost(solution_start, city_start)
    # heur = 0

    node_start = Node(city_start, solution_start, heur)
    Node.n_nodes_created += 1

    heap = Q.PriorityQueue()  # This is our heap with where we store nodes being explored
    node_start.explore_node(heap)

    not_found = True
    current_solution = None

    while not_found:
        # Each time we take the best solution found from the heap and continue from there, bad solutions are not considered
        current_node = heap.get()  # Get removes the item from the heap
        current_solution = current_node.solution
        if not current_solution.not_visited:  # if empty
            not_found = False
        else:
            current_node.explore_node(heap)

    time_end = (time.time() - time_start)*1000
    print('Fichier :', data_file)
    print('Heuristique : MST Enhanced++ - Nearest city priority + Shortest edge to start')
    print('Chemin :', end=' ')
    current_solution.print()
    print('Noeuds créés :', Node.n_nodes_created)
    print('Noeuds explorés :', Node.n_nodes_explored)
    print('Durée de traitement :', '%.0f' % time_end, 'ms')


def isN2betterThanN1(N1, N2):
    return (N1.solution.cost + N1.heuristic_cost) >= (N2.solution.cost + N2.heuristic_cost)


if __name__ == '__main__':
    main()
