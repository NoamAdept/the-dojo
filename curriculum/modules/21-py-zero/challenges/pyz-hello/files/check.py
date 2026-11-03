#!/usr/bin/env python3
"""Run with ./check. Tests each task in your .py files and lists what still fails."""
import sys
sys.path.insert(0, ".")
sys.dont_write_bytecode = True
failed, passed = [], []

def task(name):
    def run(fn):
        try:
            fn()
            passed.append(name)
        except NotImplementedError:
            failed.append(f"{name}: not implemented yet")
        except Exception as exc:  # show the learner what broke
            failed.append(f"{name}: {exc}" if isinstance(exc, AssertionError) and str(exc) else f"{name}: {type(exc).__name__}: {exc}")
        return fn
    return run

import os

def run(script):
    assert os.path.exists(script), f"{script} does not exist yet. Create it in this folder, for example with: vim {script}"
    r = subprocess.run([sys.executable, script], capture_output=True, text=True, timeout=10)
    err = (r.stderr.strip().splitlines() or [""])[-1]
    assert r.returncode == 0, f"python3 {script} stopped with an error ({err}). Run it yourself to see which line."
    return r.stdout

import subprocess

@task("1 hello.py prints Hello, Pi!")
def _():
    out = run("hello.py")
    assert out == "Hello, Pi!\n", f"hello.py printed {out!r}; it should print exactly 'Hello, Pi!' (check the comma, capital letters and the !)"

@task("2 arith.py prints four results")
def _():
    lines = run("arith.py").split("\n")[:-1]
    assert len(lines) == 4, f"arith.py printed {len(lines)} lines; it should print 4 (one print per sum)"
    assert lines == ["3.5", "3", "1", "1024"], f"arith.py printed {lines}; expected the results of 7 / 2, 7 // 2, 7 % 2, 2 ** 10"

@task("3 label.py prints Rate 2048000 Hz")
def _():
    out = run("label.py")
    assert out == "Rate 2048000 Hz\n", f"label.py printed {out!r}; print adds one space between the things you give it, so print(\"Rate\", 2048000, \"Hz\")"

@task("4 broken.py is fixed")
def _():
    out = run("broken.py")
    assert out == "Signal found\nDone\n", f"broken.py printed {out!r}; it should print 'Signal found' then 'Done'. Text needs quotes around it."

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
