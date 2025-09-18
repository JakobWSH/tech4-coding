import pyomo.environ as pyo
import pandas as pd
from pathlib import Path

solver = "appsi_highs"
SOLVER = pyo.SolverFactory(solver)
assert SOLVER.available(), "HiGHS (appsi_highs) not available"

# --- Load cost matrix C[i,j] from your Excel file ---
# Put 05a_Matching.xlsx in the same folder as this script.
xlsx_path = Path(__file__).with_name("05a_Matching.xlsx")
if not xlsx_path.exists():
    # tiny fallback so the script still runs if the file isn't there
    # 3x3 toy costs
    import numpy as np
    df = pd.DataFrame([[4, 7, 3],
                       [2, 5, 8],
                       [6, 4, 5]],
                      index=[f"i{i}" for i in range(1,4)],
                      columns=[f"j{j}" for j in range(1,4)])
else:
    # Adjust sheet name/range if your file uses a named sheet
    df = pd.read_excel(xlsx_path, sheet_name=0, index_col=0)
    # Expect: rows = I objects, cols = J objects, values = costs
    # If your file has headers in a different layout, tweak index_col / header.
    # See pandas.read_excel docs.  # noqa
    # https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html

I = list(df.index)
J = list(df.columns)
C = {(i, j): float(df.loc[i, j]) for i in I for j in J}

# --- Model (BIP) ---
m = pyo.ConcreteModel("Assignment")
m.I = pyo.Set(initialize=I)
m.J = pyo.Set(initialize=J)

# Binary x[i,j]: 1 if i is assigned to j
m.x = pyo.Var(m.I, m.J, domain=pyo.Binary)  # Binary domain per Pyomo docs

# Each i assigned to exactly one j
def row_rule(m, i):
    return sum(m.x[i, j] for j in m.J) == 1
m.row = pyo.Constraint(m.I, rule=row_rule)

# Each j receives exactly one i
def col_rule(m, j):
    return sum(m.x[i, j] for i in m.I) == 1
m.col = pyo.Constraint(m.J, rule=col_rule)

# Minimize total cost
m.obj = pyo.Objective(expr=sum(C[i, j] * m.x[i, j] for i in m.I for j in m.J),
                      sense=pyo.minimize)

# Solve
SOLVER.solve(m, tee=False)

# Report
assignments = [(i, j) for i in m.I for j in m.J if pyo.value(m.x[i, j]) > 0.5]
total_cost = pyo.value(m.obj)
print("Assignments:", assignments)
print("Total cost:", total_cost)