"""
P1 - Events on rooms | 2024 edition of Advent of OR
Author: Francisco M Vallejo
Linkeding: https://www.linkedin.com/in/franciscovallejogt/
Github: https://github.com/currovallejo/Advent-of-OR-2024
"""

import os
from dsatur import DSatur
from typing import List, Dict
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def load_instance(filename: str):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, mode="r") as file:
        lines = file.readlines()
        header = lines[8].strip().split()
        n_nodes = int(header[0])
        edges = []
        node_set = set()
        for line in lines[9:]:
            _, i, j = line.strip().split()
            edges.append((int(i) - 1, int(j) - 1))
            node_set.add(int(i) - 1)
            node_set.add(int(j) - 1)
    nodes = sorted(node_set)
    assert len(nodes) == n_nodes, "Wrong number of nodes specified"
    return {"nodes": nodes, "edges": edges}


def group_nodes_by_color(node_sequence: List["Node"]) -> Dict[str, List[int]]:
    """
    Groups a sequence of Node objects by their color.

    Parameters:
        node_sequence (List[Node]): A list of Node objects, each with attributes:
                                    - index (int): The node's ID.
                                    - color (Color): The color assigned to the node.

    Returns:
        Dict[str, List[int]]: A dictionary where keys are color representations
                              (converted to strings) and values are lists of
                              integers representing node IDs.
    """
    color_dict = {}

    for node in node_sequence:
        try:
            # Extract node index and color
            node_id = node.index  # Node's ID
            color = str(node.color.index)  # Convert color to string for use as a key

            # Add the node ID to the corresponding color in the dictionary
            if color not in color_dict:
                color_dict[color] = []
            color_dict[color].append(node_id)
        except AttributeError as e:
            print(f"Skipping invalid node: {node}. Error: {e}")

    return color_dict


def plot_schedule(room_dict: Dict[str, List[int]]):

    # Input dictionary
    schedule = room_dict

    # Generate unique colors for each room using a colormap
    num_rooms = len(schedule)
    colors = cm.get_cmap("tab20", num_rooms)  # Use the 'tab20' colormap

    # Generate X-axis labels (Morning and Evening repeated)
    max_events = max(len(events) for events in schedule.values())
    time_labels = ["Morning", "Evening"] * (max_events // 2 + 1)
    time_labels = time_labels[:max_events]  # Ensure labels match the number of events

    # Plot settings
    fig, ax = plt.subplots(figsize=(12, 8))
    y_offset = 0  # Vertical position for the bars

    # Plot each room and its events
    for idx, (room, events) in enumerate(schedule.items()):
        x_values = range(len(events))  # Events are spaced equally
        y_values = [y_offset] * len(events)  # Keep events on the same horizontal line
        ax.scatter(
            x_values, y_values, label=f"Room {room}", s=100, color=colors(idx)
        )  # Unique color for each room
        for i, event in enumerate(events):
            ax.text(
                x_values[i], y_values[i] + 0.2, f"{event}", ha="center", fontsize=9
            )  # Annotate events
        y_offset += 1  # Move to the next room

    # Formatting
    ax.set_title(
        "Event Schedule for a Congress Avoiding Overlapping Events in the same Room",
        fontsize=16,
    )
    ax.set_xlabel("Time of Day", fontsize=12)
    ax.set_ylabel("Rooms", fontsize=12)
    ax.set_yticks(range(len(schedule)))
    ax.set_yticklabels([f"Room {room}" for room in schedule.keys()], fontsize=10)
    ax.set_xticks(range(max_events))
    ax.set_xticklabels(time_labels[:max_events], rotation=45, fontsize=10)
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=8)
    plt.tight_layout()
    plt.show()


def main():

    # load instance
    my_instance = load_instance("instance.txt")

    # solve instance with heuristic Dsatur
    heuristic = DSatur(my_instance["nodes"], my_instance["edges"])
    heuristic.solve(save_history=True)
    print(f"Number of rooms needed: {heuristic.cost}")

    # get which events are assigned to each room
    sequence = heuristic.history
    room_dict = group_nodes_by_color(sequence)
    print(room_dict)

    # plot schedule
    plot_schedule(room_dict)


if __name__ == "__main__":
    main()
