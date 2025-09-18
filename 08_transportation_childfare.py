import pyomo.environ as pyo

solver = "appsi_highs"
SOLVER = pyo.SolverFactory(solver); assert SOLVER.available()

# Distances in miles (slide table)
dist = [
    [800, 1300, 400, 700],   # Plant 1 → DC1..4
    [1100, 1400, 600, 1000], # Plant 2
    [600, 1200, 800, 900],   # Plant 3
]
plants = range(3); dcs = range(4)

# Costs = 100 + 0.5 * miles
costs = [[100 + 0.5*dist[i][j] for j in dcs] for i in plants]

supply = [12, 17, 11]
demand = [10, 10, 10, 10]

m = pyo.ConcreteModel("Childfare Transportation")

# x[i,j] ≥ 0 = shipments from plant i to DC j
m.x = pyo.Var(plants, dcs, domain=pyo.NonNegativeReals)

# Objective: minimize total cost
m.total_cost = pyo.Objective(
    sense=pyo.minimize,
    expr=sum(costs[i][j] * m.x[i, j] for i, j in m.x.keys())
)

# Cannery/Plant constraints (== supply)
m.plant = pyo.ConstraintList()
for i in plants:
    m.plant.add(sum(m.x[i, j] for j in dcs) == supply[i])

# DC constraints (== demand)
m.dc = pyo.ConstraintList()
for j in dcs:
    m.dc.add(sum(m.x[i, j] for i in plants) == demand[j])

SOLVER.solve(m)
print("Total cost:", pyo.value(m.total_cost))
for (i, j) in m.x:
    v = pyo.value(m.x[i, j])
    if v > 1e-8:
        print(f"Plant {i+1} → DC{j+1}: {v}")