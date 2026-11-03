# Task 3: C++20 is required
import os, re, sys
from cmake_helper import build, run
if not os.path.isfile("projects/calculator/CMakeLists.txt"):
    sys.exit("projects/calculator/CMakeLists.txt does not exist yet")
text = open("projects/calculator/CMakeLists.txt").read()
if not re.search(r"CMAKE_CXX_STANDARD\s+20", text) or not re.search(r"CMAKE_CXX_STANDARD_REQUIRED\s+ON", text):
    sys.exit("set CMAKE_CXX_STANDARD 20 and CMAKE_CXX_STANDARD_REQUIRED ON")
out = build("projects/calculator", target="run_calc")
assert run(os.path.join(out, "run_calc")).strip() == "ui+history ok"
