#!/usr/bin/env python3
"""Run with ./check. Tests each task in tasks.py and lists what still fails."""
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

import os, random, subprocess, tempfile

def load(name):
    try:
        return __import__(name)
    except Exception as exc:
        print(f"Could not load {name}.py. Python said: {type(exc).__name__}: {exc}")
        print(f"Run  python3 {name}.py  yourself to see the full error and its line number, fix it, then run ./check again.")
        raise SystemExit(1)

def same(got, want, call):
    if got is None and want is not None:
        raise AssertionError(f"{call} gave back None. Did you forget `return`, or use print() instead of return?")
    assert got == want, f"{call} returned {got!r}, but it should return {want!r}"

tasks = load("tasks")
rng = random.Random(4)

@task("1 is_even")
def _():
    for n in [0, 1, 2, 7, -4, -3, rng.randint(1000, 9999)]:
        same(tasks.is_even(n), n % 2 == 0, f"is_even({n})")

@task("2 sign")
def _():
    for n, want in [(-5, "negative"), (0, "zero"), (3, "positive"), (-0.5, "negative"), (0.1, "positive")]:
        same(tasks.sign(n), want, f"sign({n})")

@task("3 band, including the boundaries")
def _():
    cases = [(0.5, "HF"), (29.9, "HF"), (30, "VHF"), (145.8, "VHF"), (299.99, "VHF"),
             (300, "UHF"), (433.92, "UHF"), (2999, "UHF"), (3000, "SHF"), (10000, "SHF")]
    for mhz, want in cases:
        same(tasks.band(mhz), want, f"band({mhz})")

@task("4 can_listen")
def _():
    for a in (True, False):
        for b in (True, False):
            same(tasks.can_listen(a, b), a and b, f"can_listen({a}, {b})")

@task("5 largest without max")
def _():
    nums = [rng.randint(-50, 50) for _ in range(3)]
    for a, b, c in [(1, 2, 3), (3, 2, 1), (2, 3, 1), (5, 5, 1), (-1, -7, -3), tuple(nums)]:
        same(tasks.largest(a, b, c), max(a, b, c), f"largest({a}, {b}, {c})")
    import ast, inspect, textwrap
    tree = ast.parse(textwrap.dedent(inspect.getsource(tasks.largest)))
    calls = [n.func.id for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)]
    assert "max" not in calls, "solve largest with if/elif/else instead of the built-in max()"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
