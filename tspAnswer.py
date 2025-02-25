"""
Module for solving the Traveling Salesman Problem (TSP) using a branch-and-bound/backtracking approach.

Provides functions to compute the optimal tour and total cost for a given directed graph.
"""

import sys

def runNewSolution(dg, start):
    """
    Solves the TSP for the directed graph 'dg' starting from the given vertex.
    Uses a hybrid branch-and-bound/backtracking approach with heuristic ordering.

    Args:
        dg (DGraph): The directed graph instance.
        start (int): The starting vertex index.

    Returns:
        tuple: A tuple (best_cost, best_path) where best_path includes the return to the start.
    """
    visited = [False] * dg.V
    visited[start] = True
    best = {"cost": float("inf"), "path": []}
    tsp_recursive(dg, current=start, start=start, count=1, cost=0,
                  visited=visited, current_path=[start], best=best)
    return best["cost"], best["path"]


def tsp_recursive(dg, current, start, count, cost, visited, current_path, best):
    """Recursive helper function to solve TSP via branch-and-bound.

    Args:
        dg (DGraph): The directed graph instance.
        current (int): The current vertex index.
        start (int): The starting vertex index.
        count (int): The number of vertices visited so far.
        cost (int): The accumulated travel cost.
        visited (list): A boolean list indicating visited vertices.
        current_path (list): The current path represented as a list of vertex indices.
        best (dict): Dictionary storing the best cost and corresponding path found.

    Returns:
        None: Updates the best solution in place.
    """
    # Base case: all vertices visited. Complete the cycle by returning to start.
    if count == dg.V:
        weight, vertex, _ = dg.find_node(current, start)
        if weight != sys.maxsize:  # Valid edge exists from current back to start.
            total_cost = cost + weight
            if total_cost < best["cost"]:
                best["cost"] = total_cost
                best["path"] = current_path[:] + [start]
        return

    # Prune if current cost already exceeds the best cost found.
    if cost >= best["cost"]:
        return

    # Generate candidate moves: iterate over unvisited vertices with a valid edge from current.
    candidates = []
    for v in range(dg.V):
        if not visited[v]:
            weight, vertex, _ = dg.find_node(current, v)
            if weight != sys.maxsize:
                candidates.append((v, weight))
    # Order candidates by edge weight (heuristic: lower weight first)
    candidates.sort(key=lambda x: x[1])

    # Explore each candidate recursively.
    for v, weight in candidates:
        visited[v] = True
        current_path.append(v)
        tsp_recursive(dg, current=v, start=start, count=count + 1, cost=cost + weight,
                      visited=visited, current_path=current_path, best=best)
        current_path.pop()
        visited[v] = False


# # --- Example Usage ---
# if __name__ == "__main__":
#     # Create a graph with 4 vertices (0, 1, 2, 3)
#     dg = DGraph(4)
#
#     # Add edges to the graph using your add_edge method.
#     # The parameters are: source, destination, weight, and a dummy path label.
#     dg.add_edge(0, 1, 10, "0->1")
#     dg.add_edge(0, 2, 15, "0->2")
#     dg.add_edge(0, 3, 20, "0->3")
#     dg.add_edge(1, 0, 10, "1->0")
#     dg.add_edge(1, 2, 35, "1->2")
#     dg.add_edge(1, 3, 25, "1->3")
#     dg.add_edge(2, 0, 15, "2->0")
#     dg.add_edge(2, 1, 35, "2->1")
#     dg.add_edge(2, 3, 30, "2->3")
#     dg.add_edge(3, 0, 20, "3->0")
#     dg.add_edge(3, 1, 25, "3->1")
#     dg.add_edge(3, 2, 30, "3->2")
#
#     # Run the TSP solution starting from vertex 0.
#     best_cost, best_path = runNewSolution(dg, start=0)
#
#     print("Optimal TSP tour:", best_path)
#     print("Optimal TSP cost:", best_cost)
