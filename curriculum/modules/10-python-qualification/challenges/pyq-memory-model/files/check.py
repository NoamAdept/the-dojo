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

import copy, gc, tasks

@task("1 is vs ==")
def _():
    assert tasks.identity_report() == (False, True)

@task("2 shallow copy shares the inner list")
def _():
    assert tasks.shallow_trap() == {"a": [1, 2, 3]}

@task("3 refcount grows")
def _():
    r = tasks.refcount_growth()
    assert len(r) == 3 and r[0] < r[1] < r[2], f"readings {r}"

@task("4 gc.collect clears a cycle")
def _():
    gc.collect()
    assert tasks.collect_cycle() > 0

@task("5 track_id")
def _():
    x = 1000
    assert tasks.track_id(x) == (x, id(x)) and tasks.int_id_changes() is True

@task("6 my_deepcopy")
def _():
    src = {"a": [1, {"b": [2, 3]}], "c": (4, 5), "d": "str"}
    dup = tasks.my_deepcopy(src)
    assert dup == src == copy.deepcopy(src)
    assert dup is not src and dup["a"] is not src["a"] and dup["a"][1]["b"] is not src["a"][1]["b"]
    assert dup["c"] is src["c"], "values that are not a list or dict should be shared, not copied"

@task("7 self-cycle needs the collector")
def _():
    gc.disable()
    try:
        assert tasks.cycle_needs_gc() == (True, False)
    finally:
        gc.enable()

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
