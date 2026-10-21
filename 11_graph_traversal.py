"""
11_graph_traversal.py
Category: Basic / Graph Algorithms

Description:
Implementation of fundamental Graph structures and traversal algorithms:
- Directed and undirected adjacency list representation
- Breadth-First Search (BFS) for reachability and shortest path in unweighted graphs
- Depth-First Search (DFS) iterative and recursive implementations
- Cycle detection for both directed (recursion stack) and undirected (parent tracking) graphs
- Topological sorting via Kahn's algorithm (indegree-based BFS for DAGs)
"""

from collections import deque
from typing import Dict, List, Set, Optional, Any


class Graph:
    """An adjacency-list graph representation supporting directed and undirected graphs."""

    def __init__(self, directed: bool = False):
        self.directed = directed
        self.adj: Dict[Any, List[Any]] = {}

    def add_vertex(self, vertex: Any) -> None:
        """Adds a vertex if it does not already exist."""
        if vertex not in self.adj:
            self.adj[vertex] = []

    def add_edge(self, u: Any, v: Any) -> None:
        """Adds an edge from vertex u to vertex v (and back if undirected)."""
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u].append(v)
        if not self.directed:
            self.adj[v].append(u)

    def bfs(self, start: Any) -> List[Any]:
        """Breadth-First Search traversal order starting from `start`."""
        if start not in self.adj:
            return []

        visited: Set[Any] = {start}
        queue: deque = deque([start])
        order: List[Any] = []

        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in self.adj.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return order

    def shortest_path_unweighted(self, start: Any, target: Any) -> Optional[List[Any]]:
        """
        Returns the shortest path (sequence of vertices) from start to target using BFS.
        Returns None if no path exists.
        """
        if start not in self.adj or target not in self.adj:
            return None
        if start == target:
            return [start]

        visited: Set[Any] = {start}
        queue: deque = deque([[start]])

        while queue:
            path = queue.popleft()
            node = path[-1]

            for neighbor in self.adj.get(node, []):
                if neighbor == target:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(path + [neighbor])
        return None

    def dfs(self, start: Any) -> List[Any]:
        """Depth-First Search traversal order starting from `start` (iterative)."""
        if start not in self.adj:
            return []

        visited: Set[Any] = set()
        stack: List[Any] = [start]
        order: List[Any] = []

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                order.append(node)
                # Traverse neighbors in natural order by pushing in reverse
                for neighbor in reversed(self.adj.get(node, [])):
                    if neighbor not in visited:
                        stack.append(neighbor)
        return order

    def has_cycle(self) -> bool:
        """
        Detects whether a cycle exists in the graph.
        - For directed graphs: uses recursion stack tracking.
        - For undirected graphs: tracks parent vertex to avoid false positive via the same edge.
        """
        if self.directed:
            visited: Set[Any] = set()
            rec_stack: Set[Any] = set()

            def _dfs_cycle(node: Any) -> bool:
                visited.add(node)
                rec_stack.add(node)
                for neighbor in self.adj.get(node, []):
                    if neighbor not in visited:
                        if _dfs_cycle(neighbor):
                            return True
                    elif neighbor in rec_stack:
                        return True
                rec_stack.remove(node)
                return False

            for vertex in list(self.adj.keys()):
                if vertex not in visited:
                    if _dfs_cycle(vertex):
                        return True
            return False
        else:
            visited_undir: Set[Any] = set()

            def _dfs_undir_cycle(node: Any, parent: Any) -> bool:
                visited_undir.add(node)
                for neighbor in self.adj.get(node, []):
                    if neighbor not in visited_undir:
                        if _dfs_undir_cycle(neighbor, node):
                            return True
                    elif neighbor != parent:
                        return True
                return False

            for vertex in list(self.adj.keys()):
                if vertex not in visited_undir:
                    if _dfs_undir_cycle(vertex, None):
                        return True
            return False

    def topological_sort(self) -> Optional[List[Any]]:
        """
        Computes topological ordering using Kahn's algorithm (indegree-based BFS).
        Returns ordered list of vertices if DAG, or None if graph contains a cycle or is undirected.
        """
        if not self.directed:
            return None

        indegree = {u: 0 for u in self.adj}
        for u in self.adj:
            for v in self.adj[u]:
                indegree[v] = indegree.get(v, 0) + 1

        queue: deque = deque([u for u, deg in indegree.items() if deg == 0])
        topo_order: List[Any] = []

        while queue:
            node = queue.popleft()
            topo_order.append(node)
            for neighbor in self.adj.get(node, []):
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        if len(topo_order) != len(self.adj):
            return None  # Cycle detected; not a DAG

        return topo_order


def main():
    print("=== 11: Graph Traversal & Algorithms Demo ===")

    # 1. Undirected Graph Demonstrations
    print("\n--- 1. Undirected Graph (Social Network / Mesh) ---")
    g = Graph(directed=False)
    edges = [
        ("A", "B"), ("A", "C"),
        ("B", "D"), ("B", "E"),
        ("C", "F"), ("E", "F")
    ]
    for u, v in edges:
        g.add_edge(u, v)

    print(f"Vertices: {list(g.adj.keys())}")
    print(f"BFS from 'A': {g.bfs('A')}")
    print(f"DFS from 'A': {g.dfs('A')}")
    print(f"Shortest path 'A' -> 'F': {g.shortest_path_unweighted('A', 'F')}")
    print(f"Has cycle: {g.has_cycle()}")

    # 2. Directed Acyclic Graph (DAG) & Topological Sort
    print("\n--- 2. Directed Acyclic Graph (Course Prerequisites) ---")
    dag = Graph(directed=True)
    prereqs = [
        ("CS101", "CS201"),
        ("CS201", "CS301"),
        ("CS201", "CS305"),
        ("CS301", "CS401"),
        ("MATH101", "CS401")
    ]
    for u, v in prereqs:
        dag.add_edge(u, v)

    print(f"Topological Order: {dag.topological_sort()}")
    print(f"Has cycle: {dag.has_cycle()}")

    # 3. Directed Cyclic Graph Detection
    print("\n--- 3. Cycle Detection in Directed Graph ---")
    cyclic_graph = Graph(directed=True)
    cyclic_edges = [("Task1", "Task2"), ("Task2", "Task3"), ("Task3", "Task1")]
    for u, v in cyclic_edges:
        cyclic_graph.add_edge(u, v)

    print(f"Cyclic graph has cycle: {cyclic_graph.has_cycle()}")
    print(f"Topological sort on cyclic graph: {cyclic_graph.topological_sort()}")


if __name__ == "__main__":
    main()
