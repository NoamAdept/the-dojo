# Task 2: run_calc links ui.cpp and history.cpp
import os
from cmake_helper import build, run
out = build("projects/calculator", target="run_calc")
assert run(os.path.join(out, "run_calc")).startswith("ui+history"), "run_calc output wrong"
