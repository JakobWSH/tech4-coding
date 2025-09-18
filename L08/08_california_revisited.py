import pyomo.environ as pyo
solver = "appsi_highs"; SOLVER = pyo.SolverFactory(solver); assert SOLVER.available()

m = pyo.ConcreteModel("California Manufacturing")
m.x = pyo.Var(range(4), domain=pyo.Binary)   # 4 yes/no decisions

# Maximize net value (slide numbers)
m.net_value = pyo.Objective(
    expr=9*m.x[0] + 5*m.x[1] + 6*m.x[2] + 4*m.x[3],
    sense=pyo.maximize
)

m.cons = pyo.ConstraintList()
m.cons.add(6*m.x[0] + 3*m.x[1] + 5*m.x[2] + 2*m.x[3] <= 10)  # capital
m.cons.add(m.x[2] + m.x[3] <= 1)                             # ≤ 1 WH
m.cons.add(-m.x[0] + m.x[2] <= 0)                            # x2 ≤ x0
m.cons.add(-m.x[1] + m.x[3] <= 0)                            # x3 ≤ x1

SOLVER.solve(m)
print({f"x{j+1}": int(pyo.value(m.x[j])) for j in range(4)})
print("Total value:", pyo.value(m.net_value))