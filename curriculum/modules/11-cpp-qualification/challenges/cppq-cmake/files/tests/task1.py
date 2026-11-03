# Task 1: first CMakeLists.txt builds run_calc
import os, re, sys
from cmake_helper import build
src = "projects/calculator"
text = open(os.path.join(src, "CMakeLists.txt")).read() if os.path.exists(os.path.join(src, "CMakeLists.txt")) else ""
if not re.search(r"cmake_minimum_required\s*\(\s*VERSION\s+3\.10", text, re.I):
    sys.exit("start with cmake_minimum_required(VERSION 3.10)")
if not re.search(r"project\s*\(\s*Calculator", text):
    sys.exit("name the project Calculator")
build(src, target="run_calc")
