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
rng = random.Random(3)

@task("1 double")
def _():
    for n in [0, 7, -4, rng.randint(100, 999)]:
        same(tasks.double(n), n * 2, f"double({n})")

@task("2 greet")
def _():
    for name in ["Ada", "Pi", "Grace Hopper"]:
        same(tasks.greet(name), f"Hello, {name}!", f"greet({name!r})")

@task("3 area")
def _():
    for w, h in [(3, 4), (0, 9), (rng.randint(2, 50), rng.randint(2, 50))]:
        same(tasks.area(w, h), w * h, f"area({w}, {h})")

@task("4 to_khz")
def _():
    for hz in [1500, 1000, 433920000, 1]:
        same(tasks.to_khz(hz), hz / 1000, f"to_khz({hz})")

@task("5 average returns")
def _():
    for a, b in [(2, 4), (1, 2), (-6, 6), (rng.randint(1, 99), rng.randint(1, 99))]:
        same(tasks.average(a, b), (a + b) / 2, f"average({a}, {b})")

@task("6 quadruple uses double")
def _():
    for n in [0, 3, -5, rng.randint(10, 99)]:
        same(tasks.quadruple(n), n * 4, f"quadruple({n})")
    calls = []
    real = tasks.double
    tasks.double = lambda n: calls.append(n) or real(n)
    try:
        tasks.quadruple(5)
    finally:
        tasks.double = real
    assert len(calls) == 2, f"quadruple called double {len(calls)} time(s); call it twice: double(double(n))"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
