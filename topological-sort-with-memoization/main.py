'''
A funny way of doing a topological sort on a DAG.

This implementation does have two requirements that make it fall short of
being a true general implementation of topological_sort():

- The graph must have only one source vertex
- The source vertex must be given as an argument to topological_sort()

It's straightforward to extend this core algorithm to address these
shortcomings, but most of the humor would be lost along the way.
'''

import functools
import collections


def topological_sort(g, source):
    result = []

    @functools.cache
    def traverse(v):
        for w in g.get_neighbors(v):
            traverse(w)
        result.append(v)

    traverse(source)

    return result[::-1]


class DirectedGraph:
    def __init__(self):
        self._edges = collections.defaultdict(set)
        self._vertices = set()

    def add_edge(self, v, w):
        self._edges[v].add(w)
        self._vertices.add(v)
        self._vertices.add(w)

    def get_neighbors(self, v):
        return [*self._edges[v]]


if __name__ == '__main__':
    g = DirectedGraph()
    g.add_edge('C', 'A')
    g.add_edge('C', 'F')
    g.add_edge('A', 'B')
    g.add_edge('A', 'D')
    g.add_edge('B', 'E')
    g.add_edge('D', 'E')
    g.add_edge('F', 'E')

    #   -->A--->B--
    #  /    \      \
    # C      -->D----->E
    #  \           /
    #   ---->F-----
    #
    # This graph is taken from https://adventofcode.com/2018/day/7
    #
    # This approach does not work as a solution to that problem: This approach
    # gives an arbitrary topological sort but the problem asks for a specific
    # topological sort.

    print(topological_sort(g, 'C'))
