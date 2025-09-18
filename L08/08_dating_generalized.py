import pyomo.environ as pyo

solver = "appsi_highs"; SOLVER = pyo.SolverFactory(solver); assert SOLVER.available()

# --- tiny example: people and compatible pairs (undirected) ---
P = ["A","B","C","D","E"]
pairs = [("A","B"), ("A","C"), ("B","D"), ("C","E")]  # only these edges allowed
# optional weights (1 = just maximize #matches)
w = {e: 1.0 for e in pairs}

# normalize unordered edges (i<j) so we index once
E = [tuple(sorted(e)) for e in pairs]

m = pyo.ConcreteModel("Generalized Matching")
m.E = pyo.Set(initialize=E, dimen=2)
m.match = pyo.Var(m.E, domain=pyo.Binary)  # 1 if that pair is matched

# degree ≤ 1 for every person
def degree_rule(m, p):
    return sum(m.match[e] for e in m.E if p in e) <= 1
m.degree = pyo.Constraint(P, rule=degree_rule)

m.obj = pyo.Objective(expr=sum(w[e]*m.match[e] for e in m.E), sense=pyo.maximize)

SOLVER.solve(m)
picked = [e for e in m.E if pyo.value(m.match[e]) > 0.5]
print("Matches:", picked)
print("#Matches:", sum(1 for _ in picked))