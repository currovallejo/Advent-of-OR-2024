import random
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from VNS import VNS, plot_VNS_cost_evolution, objective_function

# data
n_components = 16
n_connections = 24
connections = [
    (1, 16),
    (2, 14),
    (3, 13),
    (4, 10),
    (5, 10),
    (6, 9),
    (7, 10),
    (8, 15),
    (9, 16),
    (10, 11),
    (11, 13),
    (12, 15),
    (13, 15),
    (14, 15),
    (15, 16),
    (4, 1),
    (13, 10),
    (8, 10),
    (9, 4),
    (14, 10),
    (3, 1),
    (1, 14),
    (6, 11),
    (4, 12),
]


def random_solution(n_components: int) -> list:
    """
    Generate a random solution
    """
    sol = [i for i in range(1, n_components + 1)]
    random.shuffle(sol)
    return sol


def plot_solution(solution, connections):

    # Map each number to its position on the x-axis based on its order in the solution
    position_map = {num: idx + 1 for idx, num in enumerate(solution)}

    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot the numbers as points on the x-axis
    x_positions = list(range(1, len(solution) + 1))
    ax.scatter(x_positions, [0] * len(solution), color="black", zorder=5)
    for idx, num in enumerate(solution):
        ax.text(idx + 1, -0.5, str(num), ha="center", fontsize=10)

    # Draw arcs for the connections
    for start, end in connections:
        if start in position_map and end in position_map:
            start_x = position_map[start]  # Get x position of start
            end_x = position_map[end]  # Get x position of end
            center = (start_x + end_x) / 2  # Center of the arc
            width = abs(end_x - start_x)  # Width of the arc (horizontal distance)
            height = width / 2  # Height proportional to the width
            arc = Arc(
                (center, 0),
                width,
                height,
                angle=0,
                theta1=0,
                theta2=180,
                color="lightgrey",
                zorder=4,
            )
            ax.add_patch(arc)

    # Adjust plot settings
    ax.set_ylim(
        -1,
        max(abs(position_map[end] - position_map[start]) for start, end in connections)
        / 2
        + 1,
    )
    ax.set_xlim(0, len(solution) + 1)
    ax.set_yticks([])
    ax.set_xlabel("Numbers")
    ax.set_title("Connections as Scaled Arcs")

    # Show the plot
    plt.tight_layout()
    plt.show()


# main
best_solution, solutions_record = VNS(n_components, connections, 600)
print(best_solution)
print("Cost: ", objective_function(best_solution, connections))
plot_solution(best_solution, connections)
plot_VNS_cost_evolution((0, 100), (0, 100), solutions_record)
