# Task 7: link Threads::Threads
import os, re, sys
from cmake_helper import build, run
text = open("projects/threads/CMakeLists.txt").read() if os.path.exists("projects/threads/CMakeLists.txt") else ""
if "Threads::Threads" not in text or not re.search(r"find_package\s*\(\s*Threads", text):
    sys.exit("use find_package(Threads REQUIRED) and link Threads::Threads")
out = build("projects/threads")
assert run(os.path.join(out, "MultithreadedApp")).strip() == "thread result 7"
