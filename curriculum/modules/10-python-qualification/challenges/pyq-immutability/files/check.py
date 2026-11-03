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

import tasks

@task("1 tuple is immutable")
def _():
    assert tasks.try_modify_tuple() is TypeError

@task("2 star unpacking")
def _():
    assert tasks.split_head((1, 2, 3, 4, 5)) == (1, [2, 3, 4, 5])
    assert tasks.split_head((9,)) == (9, [])

@task("3 Server NamedTuple")
def _():
    s = tasks.Server("10.0.0.2", True)
    assert s.address == "10.0.0.2" and s.active is True and s == ("10.0.0.2", True)
    assert tasks.Server.__annotations__ == {"address": str, "active": bool}

@task("4 frozenset as key")
def _():
    d = tasks.frozenset_key()
    assert d[frozenset({1, 2})] == "ok"

@task("5 unique_elements")
def _():
    assert tasks.unique_elements([3, 1, 3, 2, 1]) == (1, 2, 3)

@task("6 ImmutablePoint")
def _():
    p = tasks.ImmutablePoint(1, 2)
    assert (p.x, p.y) == (1, 2)
    for attr in ("x", "y", "z"):
        try:
            setattr(p, attr, 9)
        except AttributeError:
            continue
        raise AssertionError(f"setting {attr} should raise AttributeError")
    assert hasattr(tasks.ImmutablePoint, "__slots__")

@task("7 memoize with list arguments")
def _():
    calls = []
    @tasks.memoize
    def total(values, scale=1):
        calls.append(1)
        return sum(values) * scale
    assert total([1, 2, 3]) == 6 and total([1, 2, 3]) == 6
    assert len(calls) == 1, "the second call with the same list should use the cache"
    assert total([1, 2, 3], scale=2) == 12 and len(calls) == 2
    assert len(total.cache) == 2

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
