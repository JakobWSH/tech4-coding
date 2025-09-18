# 01_wyndor.py
import pyomo.environ as pyo

solver = "appsi_highs"
SOLVER = pyo.SolverFactory(solver)
assert SOLVER.available(), f"Solver {solver} is not available"

# Model
model = pyo.ConcreteModel("Wyndor Glass Co.")

# Variables with bounds 0 ≤ x1 ≤ 4, 0 ≤ x2 ≤ 6
model.x1 = pyo.Var(bounds=(0, 4))
model.x2 = pyo.Var(bounds=(0, 6))

# Constraint: 3x1 + 2x2 ≤ 18
@model.Constraint()
def plant3(m):
    return 3*m.x1 + 2*m.x2 <= 18

# Objective: max 3x1 + 5x2
@model.Objective(sense=pyo.maximize)
def profit(m):
    return 3*m.x1 + 5*m.x2

# Solve + print results
SOLVER.solve(model)
print("x1* =", pyo.value(model.x1))
print("x2* =", pyo.value(model.x2))
print("profit* =", pyo.value(model.profit))
