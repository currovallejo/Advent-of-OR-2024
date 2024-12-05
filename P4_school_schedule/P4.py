import pyomo.environ as pyo

# data
n_classes = 4
n_teachers = 4
n_rooms = 4
n_periods = 30

f = [
    [[2, 2, 1, 2], [1, 1, 1, 2], [1, 1, 1, 6], [2, 2, 3, 2]],
    [[2, 5, 1, 2], [0, 4, 3, 2], [1, 2, 1, 0], [2, 2, 1, 2]],
    [[2, 1, 1, 2], [0, 0, 5, 1], [2, 1, 4, 1], [6, 1, 2, 1]],
    [[3, 1, 2, 1], [1, 4, 1, 4], [3, 3, 2, 1], [2, 0, 1, 1]],
]

print("building model...")

# Initialize model
model = pyo.ConcreteModel()

# Define sets
model.teachers = pyo.RangeSet(0, n_teachers - 1)
model.classes = pyo.RangeSet(0, n_classes - 1)
model.rooms = pyo.RangeSet(0, n_rooms - 1)
model.periods = pyo.RangeSet(0, n_periods - 1)

# Define variables
model.x = pyo.Var(
    model.teachers, model.classes, model.rooms, model.periods, within=pyo.Binary
)

# Define objective
model.obj = pyo.Objective(
    expr=sum(
        model.x[c, t, r, p]
        for c in model.classes
        for t in model.teachers
        for r in model.rooms
        for p in model.periods
    ),
    sense=pyo.maximize,
)

# Define constraints
model.cons = pyo.ConstraintList()

for c in model.classes:
    for t in model.teachers:
        for r in model.rooms:
            model.cons.add(
                sum(model.x[c, t, r, p] for p in model.periods) == f[c][t][r]
            )

for t in model.teachers:
    for p in model.periods:
        model.cons.add(
            sum(model.x[c, t, r, p] for c in model.classes for r in model.rooms) <= 1
        )

for c in model.classes:
    for p in model.periods:
        model.cons.add(
            sum(model.x[c, t, r, p] for t in model.teachers for r in model.rooms) <= 1
        )

# Solve model
print("model built\n solving model...")
solver = pyo.SolverFactory("glpk")
solver.solve(model, tee=True)
print('Objective function value (total number of classes scheduled):', pyo.value(model.obj))
# Print results
schedule = {c: [['' for _ in range(5)] for _ in range(6)] for c in model.classes}

for c in model.classes:
    for t in model.teachers:
        for r in model.rooms:
            for p in model.periods:
                if pyo.value(model.x[c, t, r, p]) > 0.5:
                    day = p // 6
                    period = p % 6
                    schedule[c][period][day] = f'T{t}'

for c in model.classes:
    print(f"Class {c} schedule:")
    for row in schedule[c]:
        print(' '.join(row))
    print()

