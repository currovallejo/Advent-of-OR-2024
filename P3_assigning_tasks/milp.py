import pyomo.environ as pyo
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.decorators import timed


class AssignmentModel:

    def __init__(self, params):
        self.params = params
        self.model = pyo.ConcreteModel()
        self._build_model()

    def _build_sets(self):
        self.model.workers = pyo.RangeSet(1, self.params.n_workers)
        self.model.tasks = pyo.RangeSet(1, self.params.n_tasks)

    def _build_variables(self):
        self.model.x = pyo.Var(self.model.workers, self.model.tasks, within=pyo.Binary)
        self.model.c = pyo.Var(
            self.model.workers, self.model.tasks, within=pyo.NonNegativeReals
        )
        self.model.obj = pyo.Var(domain=pyo.NonNegativeReals)

    def _build_constraints(self):

        def _one_task_per_worker():
            for i in self.model.workers:
                self.model.cons.add(
                    sum(self.model.x[i, j] for j in self.model.tasks) == 1
                )

        def _one_worker_per_task():
            for j in self.model.tasks:
                self.model.cons.add(
                    sum(self.model.x[i, j] for i in self.model.workers) == 1
                )

        def _cost_per_worker():
            for i in self.model.workers:
                for j in self.model.tasks:
                    self.model.cons.add(
                        self.model.c[i, j]
                        == self.params.costs[i - 1][j - 1] * self.model.x[i, j]
                    )

        def _total_cost():
            self.model.cons.add(
                sum(
                    self.model.c[i, j]
                    for i in self.model.workers
                    for j in self.model.tasks
                )
                == self.model.obj
            )

        _one_task_per_worker()
        _one_worker_per_task()
        _cost_per_worker()
        _total_cost()

    def _build_model(self):

        print("Building model...")

        self._build_sets()
        self._build_variables()
        self.model.cons = pyo.ConstraintList()
        self._build_constraints()
        self.model.objective = pyo.Objective(expr=self.model.obj, sense=pyo.minimize)

        print("Model built.")

    @timed
    def solve_model(self):
        print("Solving model...")
        self.solver = pyo.SolverFactory("glpk")
        self.solver.options["tmlim"] = 120
        print("Model solved.")

        return self.solver.solve(self.model, tee=True)
