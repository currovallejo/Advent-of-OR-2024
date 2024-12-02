import networkx as nx
import heapq
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.decorators import timed


class Graph:
    def __init__(self, graph_dict):
        self.G = self._create_graph(graph_dict)
        self.max_cost = graph_dict["max_cost"]

    def _create_graph(self, graph_dict):
        graph = nx.DiGraph()
        graph.add_weighted_edges_from(graph_dict["edges"])

        return graph

    @timed
    def constrained_shortest_path(self, source, target):
        max_cost = self.max_cost
        graph = self.G

        # Priority queue: (distance, cost, current_node, path)
        pq = [(0, 0, source, [source])]
        visited = set()

        while pq:
            distance, cost, node, path = heapq.heappop(pq)

            # If we reach the target and within the cost constraint
            if node == target and cost <= max_cost:
                return path, distance, cost

            # Skip if already visited
            if (node, cost) in visited:
                continue
            visited.add((node, cost))

            for neighbor in graph.neighbors(node):
                edge_data = graph[node][neighbor]["weight"]  # (distance, cost)
                new_distance = distance + edge_data[0]
                new_cost = cost + edge_data[1]

                if new_cost <= max_cost:
                    heapq.heappush(
                        pq, (new_distance, new_cost, neighbor, path + [neighbor])
                    )

        return None, float("inf"), float("inf")
