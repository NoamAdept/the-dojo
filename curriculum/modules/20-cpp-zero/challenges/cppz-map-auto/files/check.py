#!/usr/bin/env python3
"""Run with ./check. Compiles and runs each tests/taskN test against your tasks.h."""
import glob, os, re, shlex, subprocess, sys, tempfile

CXX = os.environ.get("CXX", "g++")
FLAGS = ["-std=c++17", "-Wall", "-Wextra", "-pthread", "-I.", "-Itests"]
EXTRA = shlex.split(os.environ.get("ACADEMY_CXXFLAGS", "")) + shlex.split(open(".cxxflags").read() if os.path.exists(".cxxflags") else "")
LIBS = shlex.split(subprocess.run(open(".libs").read(), shell=True, capture_output=True, text=True).stdout) if os.path.exists(".libs") else []
# ponytail: tests compile one by one (simple, clear errors); a Pi 4 takes a few seconds per task.

def title(path):
    first = open(path).readline()
    m = re.match(r"\s*(?://|#)\s*(.*)", first)
    return m.group(1) if m else os.path.basename(path)

def natural(path):
    return int(re.search(r"(\d+)", os.path.basename(path)).group(1))

passed, failed = [], []
build = tempfile.mkdtemp(prefix="academy-")
for test in sorted(glob.glob("tests/task*.cpp") + glob.glob("tests/task*.py"), key=natural):
    name = title(test)
    if test.endswith(".py"):
        run = subprocess.run([sys.executable, test], capture_output=True, text=True, timeout=300)
    else:
        exe = os.path.join(build, os.path.basename(test)[:-4])
        comp = subprocess.run([CXX, *FLAGS, *EXTRA, test, "-o", exe, *LIBS], capture_output=True, text=True)
        if comp.returncode != 0:
            errors = [l for l in comp.stderr.splitlines() if "error" in l][:3] or comp.stderr.splitlines()[:3]
            failed.append(f"{name}: does not compile yet\n      " + "\n      ".join(errors))
            continue
        try:
            run = subprocess.run([exe], capture_output=True, text=True, timeout=60)
        except subprocess.TimeoutExpired:
            failed.append(f"{name}: timed out (infinite loop or deadlock?)")
            continue
    if run.returncode == 0:
        passed.append(name)
    else:
        detail = (run.stderr or run.stdout).strip().splitlines()[-3:]
        failed.append(f"{name}: " + (" | ".join(detail) or f"exit code {run.returncode}"))

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
