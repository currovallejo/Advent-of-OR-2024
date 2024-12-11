import time
import random
import matplotlib.pyplot as plt


def objective_function(solution: list, connections: list[tuple]) -> float:
    """
    Evaluate the solution based on the parameters
    """
    cost = 0
    already_checked = []
    for connection_1 in connections:
        already_checked.append(connection_1)
        c11_i = min(solution.index(connection_1[0]), solution.index(connection_1[1]))
        c12_i = max(solution.index(connection_1[0]), solution.index(connection_1[1]))
        if abs(c11_i - c12_i) > 1:
            for connection_2 in connections:
                if connection_2 not in already_checked:
                    c21_i = min(
                        solution.index(connection_2[0]), solution.index(connection_2[1])
                    )
                    c22_i = max(
                        solution.index(connection_2[0]), solution.index(connection_2[1])
                    )
                    if abs(c21_i - c22_i) > 1:
                        if c21_i < c11_i and c11_i < c22_i < c12_i:
                            cost += 1
                        if c11_i < c21_i < c12_i and c22_i > c12_i:
                            cost += 1

    return cost


def random_neighbour_SWAP(solution: list):
    neighbour = solution[:]
    while True:
        i = random.randint(0, len(solution) - 1)
        j = random.randint(0, len(solution) - 1)
        if i != j:
            neighbour[i], neighbour[j] = neighbour[j], neighbour[i]
            return neighbour


def random_neighbour_INSERTION(solution: list):
    neighbour = solution[:]
    while True:
        i = random.randint(0, len(solution) - 1)
        j = random.randint(0, len(solution) - 1)
        if j != i:
            extracted = neighbour.pop(i)
            neighbour.insert(j, extracted)
            return neighbour


def mod_partial_search_neighbourhood_SWAP(solution: list, connections: list[tuple]):
    neighbourhood = []
    found_better_solution = False
    for i in range(len(solution) - 1):
        for j in range(i + 1, len(solution)):
            neighbour = solution[:]
            neighbour[i], neighbour[j] = neighbour[j], neighbour[i]
            neighbourhood.append(neighbour)
            if objective_function(neighbour, connections) < objective_function(
                solution, connections
            ):
                solution = neighbour
                found_better_solution = True
                break

        if found_better_solution is True:
            break

    return solution, found_better_solution


def mod_partial_search_neighbourhood_INSERTION(
    solution: list, connections: list[tuple]
):  # non recursive function. Explores only one neighbourhood.

    neighbourhood = []
    found_better_solution = False

    for i in range(len(solution)):
        solution_copy = solution[:]
        extracted = solution_copy.pop(i)
        for j in range(len(solution)):
            if i != j and j != i - 1:
                solution_copy.insert(j, extracted)
                if objective_function(solution_copy, connections) < objective_function(
                    solution, connections
                ):
                    solution = solution_copy
                    found_better_solution = True
                    break
                else:
                    solution_copy2 = solution_copy[:]
                    neighbourhood.append(solution_copy2)
                    solution_copy.pop(j)
        if found_better_solution:
            break

    return solution, found_better_solution


def shaking(solution: list, k: int):
    # random solution k_0
    if k == 0:
        new_solution = random_neighbour_SWAP(solution)

    if k == 1:
        new_solution = random_neighbour_INSERTION(solution)

    return new_solution


def VNS(n_components: int, connections: list[tuple], stop_value):
    best_solution = [i for i in range(1, n_components + 1)]
    random.shuffle(best_solution)
    solutions_record = []
    iteration_cycle = 1
    k = 0
    start_time_VNS = time.time()
    while True:
        actual_time_VNS = time.time()
        if actual_time_VNS - start_time_VNS < stop_value:  # time stop condition
            while k <= 1:
                # shaking phase
                current_solution = shaking(best_solution, k)

                # VND phase
                j = 0
                while j <= 1:
                    j = 0
                    if j == 0:
                        new_solution, solution_has_improved = (
                            mod_partial_search_neighbourhood_SWAP(
                                current_solution, connections
                            )
                        )
                        if solution_has_improved:
                            current_solution = new_solution
                            current_cost = objective_function(
                                current_solution, connections
                            )
                            solutions_record.append(
                                (
                                    current_cost,
                                    current_solution,
                                    "SWAP",
                                    iteration_cycle,
                                )
                            )
                            iteration_cycle += 1
                        else:
                            j = 1
                    if j == 1:
                        new_solution, solution_has_improved = (
                            mod_partial_search_neighbourhood_INSERTION(
                                current_solution, connections
                            )
                        )
                        if solution_has_improved:
                            current_solution = new_solution
                            current_cost = objective_function(
                                current_solution, connections
                            )
                            solutions_record.append(
                                (
                                    current_cost,
                                    current_solution,
                                    "INSERTION",
                                    iteration_cycle,
                                )
                            )
                            iteration_cycle += 1
                        else:
                            j = 2

                if current_cost < objective_function(best_solution, connections):
                    best_solution = current_solution
                    k = 0
                else:
                    k += 1

        else:
            break

    return best_solution, solutions_record


def plot_VNS_cost_evolution(x_lim, y_lim, solutions_record):
    costs = []
    swap_costs = []
    swap_cycles = []
    insertion_costs = []
    insertion_cycles = []
    cycles = list(range(1, len(solutions_record) + 1))
    for solution in solutions_record:
        costs.append(solution[0])
        if solution[2] == "SWAP":
            swap_costs.append(solution[0])
            swap_cycles.append(solution[3])
        else:
            insertion_costs.append(solution[0])
            insertion_cycles.append(solution[3])
    plt.title("VNS algorithm cost evolution")
    plt.xlim(x_lim[0], x_lim[1])
    plt.ylim(y_lim[0], y_lim[1])
    plt.xlabel("iteration cycle")
    plt.ylabel("solution cost")
    plt.plot(cycles, costs)
    plt.scatter(swap_cycles, swap_costs, c="red", label="SWAP")
    plt.scatter(insertion_cycles, insertion_costs, c="b", label="INSERTION")
    plt.legend()
    for i in range(len(cycles) - 1):
        if solutions_record[i][2] != solutions_record[i + 1][2]:
            plt.axvline(x=solutions_record[i][3] + 0.5, color="black", linestyle="--")
    plt.show()
