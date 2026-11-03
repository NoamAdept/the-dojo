# Task 2: CMake find_package + target_link_libraries
import re, sys
try:
    text = open("deps.cmake").read()
except FileNotFoundError:
    sys.exit("create deps.cmake")
assert re.search(r"find_package\s*\(\s*nlohmann_json\s+CONFIG\s+REQUIRED\s*\)", text), "find_package line"
assert re.search(r"target_link_libraries\s*\(\s*app\s+PRIVATE\s+nlohmann_json::nlohmann_json\s*\)", text), "link line"
