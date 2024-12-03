"""
P3 - Assigning tasks | 2024 edition of Advent of OR
Author: Francisco M Vallejo
Linkeding: https://www.linkedin.com/in/franciscovallejogt/
Github: https://github.com/currovallejo/Advent-of-OR-2024
"""

from params import TasksParams
from P3_assigning_tasks.milp import AssignmentModel


def main():
    n_tasks, n_workers, costs = TasksParams.get_params("instance.txt")
    tasks_params = TasksParams(n_tasks, n_workers, costs)
    print(len(costs))

    my_model = AssignmentModel(tasks_params)
    _ = my_model.solve_model()
    cost = my_model.model.obj()
    x_sol = my_model.model.x.get_values()

    print(f"Optimal cost: {cost}")

    for (employee, task), value in x_sol.items():
        if value == 1:  # If the assignment variable is active (value == 1)
            print(f"Employee {employee} is assigned to Task {task}")


if __name__ == "__main__":
    main()
