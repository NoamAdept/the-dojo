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

import math
tasks = load("tasks")
rng = random.Random(5)

@task("1 sum_to")
def _():
    for n in [0, 1, 5, 100, rng.randint(200, 900)]:
        same(tasks.sum_to(n), n * (n + 1) // 2, f"sum_to({n})")

@task("2 countdown")
def _():
    for n in [3, 1, 0, 10]:
        want = "".join(f"{i} " for i in range(n, 0, -1)) + "liftoff"
        same(tasks.countdown(n), want, f"countdown({n})")

@task("3 factorial")
def _():
    for n in [0, 1, 5, 10, rng.randint(15, 25)]:
        same(tasks.factorial(n), math.factorial(n), f"factorial({n})")

@task("4 count_multiples")
def _():
    for n, k in [(10, 3), (10, 1), (5, 7), (100, 10), (rng.randint(50, 500), rng.randint(2, 9))]:
        same(tasks.count_multiples(n, k), n // k, f"count_multiples({n}, {k})")

@task("5 count_digits")
def _():
    for n in [0, 7, 10, 99, 100, 123456, rng.randint(10**8, 10**9)]:
        same(tasks.count_digits(n), len(str(n)), f"count_digits({n})")

@task("6 first_power_over")
def _():
    for limit in [0, 1, 2, 5, 8, 1000, rng.randint(10**5, 10**6)]:
        want = 1
        while want <= limit:
            want *= 2
        same(tasks.first_power_over(limit), want, f"first_power_over({limit})")

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
