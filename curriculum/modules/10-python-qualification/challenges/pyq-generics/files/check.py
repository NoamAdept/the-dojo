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

import typing, tasks

@task("1 swap")
def _():
    assert tasks.swap(1, 2) == (2, 1)
    hints = typing.get_type_hints(tasks.swap)
    assert hints.get("a") is tasks.T and hints.get("return") == tuple[tasks.T, tasks.T], hints

@task("2 Clickable protocol")
def _():
    class Button:
        def click(self):
            return "clicked"
    assert tasks.process_click(Button()) == "clicked" and isinstance(Button(), tasks.Clickable)
    try:
        tasks.process_click(object())
    except TypeError:
        pass
    else:
        raise AssertionError("non-Clickable should raise TypeError")

@task("3 Literal status")
def _():
    assert typing.get_args(tasks.Status) == ("IDLE", "RUNNING", "ERROR")
    assert tasks.set_status("RUNNING") == "RUNNING"
    try:
        tasks.set_status("SLEEPING")
    except ValueError:
        pass
    else:
        raise AssertionError("unknown status should raise ValueError")

@task("4 Car TypedDict")
def _():
    assert typing.get_type_hints(tasks.Car) == {"make": str, "model": str, "year": int}
    car: tasks.Car = {"make": "VW", "model": "T2", "year": 1972}
    assert car["year"] == 1972

@task("5 Stack[T]")
def _():
    assert typing.Generic in tasks.Stack.__mro__
    s = tasks.Stack[int]()
    s.push(1); s.push(2)
    assert s.peek() == 2 and s.pop() == 2 and len(s) == 1 and s.pop() == 1
    try:
        s.pop()
    except IndexError:
        pass
    else:
        raise AssertionError("empty pop should raise IndexError")

@task("6 Observable[T]")
def _():
    got = []
    o = tasks.Observable[str]()
    o.subscribe(got.append)
    o.subscribe(lambda s: got.append(s.upper()))
    o.notify("rx")
    assert got == ["rx", "RX"]

@task("7 PluginManager")
def _():
    m = tasks.PluginManager()
    m.register(tasks.AuthPlugin())
    m.register(tasks.LogPlugin())
    out = m.run_all({"user": "noam"})
    assert out["auth"] is True and out["log"] == [tasks.LogPlugin().name()] and out["user"] == "noam"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
