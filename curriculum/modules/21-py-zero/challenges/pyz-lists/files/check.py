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
rng = random.Random(6)

def rand_list(k):
    return [rng.randint(-20, 40) for _ in range(k)]

def untouched(fn, items, *extra):
    copy = list(items)
    result = fn(items, *extra)
    assert items == copy, f"{fn.__name__} changed the list that it got. Build a new list instead."
    return result

@task("1 ends")
def _():
    for items in [[4, 8, 15, 16], ["a", "b"], [7], rand_list(9)]:
        same(untouched(tasks.ends, items), [items[0], items[-1]], f"ends({items})")

@task("2 middle")
def _():
    for items in [[4, 8, 15, 16], [1, 2], [1, 2, 3], rand_list(8)]:
        same(untouched(tasks.middle, items), items[1:-1], f"middle({items})")

@task("3 evens_up_to")
def _():
    for n in [7, 8, 0, 1, rng.randint(20, 60)]:
        same(tasks.evens_up_to(n), list(range(0, n + 1, 2)), f"evens_up_to({n})")

@task("4 count_above")
def _():
    for items, limit in [([1, 5, 9, 5], 5), ([], 0), (rand_list(15), 10)]:
        want = len([x for x in items if x > limit])
        same(untouched(tasks.count_above, items, limit), want, f"count_above({items}, {limit})")

@task("5 average")
def _():
    for items in [[2, 4], [5], [1, 2, 3, 4], rand_list(11)]:
        got = untouched(tasks.average, items)
        assert got is not None, f"average({items}) gave back None. Did you forget return?"
        assert abs(got - sum(items) / len(items)) < 1e-9, f"average({items}) returned {got}, but it should return {sum(items) / len(items)}"

@task("6 squares with a list comprehension")
def _():
    for n in [0, 1, 5, rng.randint(10, 30)]:
        same(tasks.squares(n), [i * i for i in range(n)], f"squares({n})")
    import ast, inspect, textwrap
    tree = ast.parse(textwrap.dedent(inspect.getsource(tasks.squares)))
    assert any(isinstance(node, ast.ListComp) for node in ast.walk(tree)), "write squares as a list comprehension: return [i * i for i in range(n)]"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
