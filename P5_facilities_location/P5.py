import pyomo.environ as pyo
import os


print("loading data...")
# data
n_warehouses = 16
n_clients = 50
q = [5000 for i in range(n_warehouses)]
f = [7500 if i != 10 else 0 for i in range(n_warehouses)]

# data from the file
filepath = os.path.join(os.path.dirname(__file__), "instance.txt")
with open(filepath, "r") as file:
    lines = file.readlines()
    data_lines = lines[29:]
    demand = []
    costs = []

    for i in range(0, len(data_lines), 4):
        client_costs = []
        demand.append(int(data_lines[i].strip()))
        client_costs.append((data_lines[i + j].strip().split()) for j in range(1, 4))
        client_costs = [
            float(num) for j in range(1, 4) for num in data_lines[i + j].strip().split()
        ]
        costs.append(client_costs)


print("data loaded\n building model...")

# Initialize model
model = pyo.ConcreteModel()

# Define sets
model.warehouses = pyo.RangeSet(0, n_warehouses - 1)
model.clients = pyo.RangeSet(0, n_clients - 1)

# Define variables
# model.x = pyo.Var(model.clients, model.warehouses, within=pyo.Binary)
# to get a feasible solution, we need to split the demand of clients among the warehouses
model.x = pyo.Var(model.clients, model.warehouses, within=pyo.UnitInterval)
model.u = pyo.Var(model.warehouses, within=pyo.Binary)
# auxiliary variable to ensure integer values when splitting the demand
model.z = pyo.Var(model.clients, model.warehouses, within=pyo.NonNegativeIntegers)


# Define objective
model.obj = pyo.Objective(
    expr=sum(
        costs[c][w] * model.x[c, w] for w in model.warehouses for c in model.clients
    )
    + sum(f[w] * model.u[w] for w in model.warehouses),
    sense=pyo.minimize,
)

# Define constraints
model.cons = pyo.ConstraintList()

for w in model.warehouses:
    model.cons.add(sum(model.x[c, w] * demand[c] for c in model.clients) <= q[w])

for w in model.warehouses:
    for c in model.clients:
        model.cons.add(model.u[w] >= model.x[c, w])
        model.cons.add(model.z[c, w] <= demand[c] * model.x[c, w])
        model.cons.add(
            model.z[c, w] >= demand[c] * model.x[c, w] - (1 - model.x[c, w]) * demand[c]
        )


for c in model.clients:
    model.cons.add(sum(model.x[c, w] for w in model.warehouses) == 1)


with open("model_output.txt", "w") as f:
    model.pprint(ostream=f)


# Solve
print("model built\n solving...")
solver = pyo.SolverFactory("glpk")
solver.solve(model, tee=True)
print("model solved\n")

# Print results
print("Results:")
print("Objective value (costs): ", pyo.value(model.obj))
print("Warehouses to open: ", [w for w in model.warehouses if pyo.value(model.u[w])])
for w in model.warehouses:
    print(f"Warehouse {w}:")
    for c in model.clients:
        if pyo.value(model.x[c, w]) > 0:
            print(f"  Client {c}: {pyo.value(model.x[c, w]) * demand[c]}")
