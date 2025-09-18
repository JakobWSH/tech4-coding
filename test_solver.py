# test_solver.py
import pyomo.environ as pyo

solver = "appsi_highs"   # HiGHS via Pyomo APPSI
SOLVER = pyo.SolverFactory(solver)
assert SOLVER.available(), f"Solver {solver} is not available"

print("OK: HiGHS is available via Pyomo (appsi_highs).")
