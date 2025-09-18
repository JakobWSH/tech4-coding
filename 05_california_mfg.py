import pyomo.environ as pyo

solver = "appsi_highs"
SOLVER = pyo.SolverFactory(solver)
assert SOLVER.available(), "HiGHS (appsi_highs) not available"

m = pyo.ConcreteModel("California_Mfg")

# x1..x4 are yes/no decisions: LA factory, SF factory, LA warehouse, SF warehouse
m.J = pyo.RangeSet(1, 4)
m.x = pyo.Var(m.J, domain=pyo.Binary)

# Data from the slide table (NPV, capital) — see Lecture 5 “Prototype Example”
NPV = {1: 9, 2: 5, 3: 6, 4: 4}      # in $M
CAP = {1: 6, 2: 3, 3: 5, 4: 2}      # in $M
BUDGET = 10

# Objective: maximize total NPV
m.obj = pyo.Objective(expr=sum(NPV[j] * m.x[j] for j in m.J), sense=pyo.maximize)

# Capital constraint
m.cap = pyo.Constraint(expr=sum(CAP[j] * m.x[j] for j in m.J) <= BUDGET)

# Logic: a warehouse can be built only if its city has a factory
m.dep_LA = pyo.Constraint(expr=m.x[3] <= m.x[1])  # x3 <= x1
m.dep_SF = pyo.Constraint(expr=m.x[4] <= m.x[2])  # x4 <= x2

# At most one warehouse overall (as described)
m.at_most_one_wh = pyo.Constraint(expr=m.x[3] + m.x[4] <= 1)

SOLVER.solve(m, tee=False)

print({f"x{j}": int(pyo.value(m.x[j])) for j in m.J})
print("Total NPV:", pyo.value(m.obj))
print("Total capital used:", sum(CAP[j]*pyo.value(m.x[j]) for j in m.J))