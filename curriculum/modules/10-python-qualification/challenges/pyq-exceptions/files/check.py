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

import contextlib, io, math, tasks

def quiet(fn, *a, **k):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        return fn(*a, **k), buf.getvalue()

@task("1 read_int")
def _():
    value, out = quiet(tasks.read_int, iter(["x", "4.5", "12", "99"]))
    assert value == 12 and out.count("Invalid") == 2

@task("2 safe_get")
def _():
    assert tasks.safe_get([1, 2, 3], 1) == 2 and tasks.safe_get([1, 2, 3], 10) is None

@task("3 InvalidAgeError")
def _():
    assert tasks.set_age(40) == 40
    for bad in (-1, 151):
        try:
            tasks.set_age(bad)
        except tasks.InvalidAgeError:
            continue
        raise AssertionError(f"set_age({bad}) should raise InvalidAgeError")

@task("4 try/finally cleanup")
def _():
    log = []
    tasks.use_resource(log, False)
    try:
        tasks.use_resource(log, True)
    except RuntimeError:
        pass
    else:
        raise AssertionError("fail=True should raise RuntimeError")
    assert log == ["open", "closed", "open", "closed"], log

@task("5 safe_divide")
def _():
    assert tasks.safe_divide(1, 4) == 0.25 and math.isinf(tasks.safe_divide(1, 0))
    value, out = quiet(tasks.safe_divide, "a", 2)
    assert value is None and "Inputs must be numbers" in out

@task("6 retry")
def _():
    calls = []
    @tasks.retry(attempts=3)
    def flaky():
        calls.append(1)
        if len(calls) < 3:
            raise IOError("not yet")
        return "ok"
    value, out = quiet(flaky)
    assert value == "ok" and len(calls) == 3 and out.count("Retrying...") == 2
    @tasks.retry(attempts=2)
    def broken():
        raise KeyError("always")
    try:
        quiet(broken)
    except KeyError:
        pass
    else:
        raise AssertionError("should re-raise the last exception")

@task("7 process_batch keeps going")
def _():
    accts = {n: tasks.Account(n, b) for n, b in [("a", 100), ("b", 0)]}
    done, errors = tasks.process_batch([("a", "b", 30), ("b", "a", 999), ("a", "zz", 1), ("a", "b", 70)], accts)
    assert done == 2 and len(errors) == 2, (done, errors)
    assert accts["a"].balance == 0 and accts["b"].balance == 100
    try:
        accts["b"].transfer(1000, "a", accts)
    except tasks.InsufficientFunds:
        pass
    else:
        raise AssertionError("expected InsufficientFunds")

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
