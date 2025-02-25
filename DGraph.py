"""
Module for representing a directed graph using an adjacency list.

Implements the DGraph class, which uses linked lists (via AdjNode) to represent edges
with associated weights and path details.
"""

import sys

class AdjNode:
    """Node in the adjacency list representing a directed edge in the graph."""

    def __init__(self, value, weight, path):
        """Initialize an adjacency node.

        Args:
            value (int): The destination vertex index.
            weight (int): The weight of the edge (e.g., travel time).
            path (object): The Path object associated with this edge.
        """
        self.vertex = value
        self.weight = weight
        self.next = None
        self.path = path


class DGraph:
    """Directed graph implemented using an adjacency list."""

    def __init__(self, num):
        """Initialize the directed graph.

        Args:
            num (int): The number of vertices in the graph.
        """
        self.V = num
        self.graph = [None] * self.V

    def add_edge(self, s, d, w, p):
        """Add a directed edge to the graph.

        Args:
            s (int): The source vertex index.
            d (int): The destination vertex index.
            w (int): The weight of the edge.
            p (object): The Path object associated with the edge.
        """
        node = AdjNode(d, w, p)
        node.next = self.graph[s]
        self.graph[s] = node

    def find_node(self, bucket, index):
        """Find and return edge information from a given source vertex.

        Args:
            bucket (int): The index of the source vertex.
            index (int): The destination vertex index to search for.

        Returns:
            tuple: (weight, vertex, path) if the edge exists; otherwise, (sys.maxsize, sys.maxsize, sys.maxsize).
        """
        cur = self.graph[bucket]
        while cur is not None:
            if index == cur.vertex:
                return cur.weight, cur.vertex, cur.path
            cur = cur.next
        return sys.maxsize, sys.maxsize, sys.maxsize

    def print_graph(self):
        """Print the graph's adjacency list for debugging purposes."""
        for i in range(self.V):
            print("Vertex " + str(i) + ":", end="")
            temp = self.graph[i]
            while temp:
                print(" -> {} = {}".format(temp.vertex, temp.weight), end="")
                temp = temp.next
            print(" \n")
