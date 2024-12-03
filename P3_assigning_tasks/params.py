import os


class TasksParams:

    def __init__(self, n_tasks: int, n_workers: int, costs: list[list[int]]):
        self.n_tasks = n_tasks
        self.n_workers = n_workers
        self.costs = costs

    @staticmethod
    def get_params(filename: str):
        filepath = os.path.join(os.path.dirname(__file__), filename)
        with open(filepath, "r") as f:
            lines = f.readlines()
            data_lines = lines[9:]
            n_tasks = n_workers = int(data_lines[0])
            data_lines = data_lines[1:]
            employee_costs = []
            costs = []
            for line in data_lines:
                if len(costs) == n_tasks:
                    employee_costs.append(costs)
                    costs = []
                    costs = costs + [int(x) for x in line.split()]
                else:
                    costs = costs + [int(x) for x in line.split()]
            employee_costs.append(costs)

        return n_tasks, n_workers, employee_costs
