import os
import dijkstra


def load_instance(filename: str):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, mode="r") as file:
        lines = file.readlines()
        header = lines[13].strip().split()
        n_nodes = int(header[0])
        max_cost = int(header[2])
        edges = []
        for line in lines[14:]:
            i, j, d, c = line.strip().split()
            edges.append((int(i), int(j), (int(d), int(c))))
    nodes = set(range(1, n_nodes + 1))
    assert len(nodes) == n_nodes, "Wrong number of nodes specified"
    return {"nodes": nodes, "edges": edges, "max_cost": max_cost}


def main():
    instance = load_instance("instance.txt")
    G = dijkstra.Graph(instance)
    path, distance, cost = G.constrained_shortest_path(1, 100)
    print("Path:", path)
    print("Distance:", distance)
    print("Cost:", cost)


if __name__ == "__main__":
    main()
