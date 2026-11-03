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

import contextlib, inspect, io, os, tempfile, tasks

@task("1 log_call")
def _():
    @tasks.log_call
    def tune(f):
        return f * 2
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        assert tune(5) == 10
    assert "Calling tune" in buf.getvalue() and tune.__name__ == "tune"

@task("2 squares generator")
def _():
    g = tasks.squares(4)
    assert inspect.isgenerator(g) and list(g) == [0, 1, 4, 9, 16]

@task("3 compare_join")
def _():
    j, c = tasks.compare_join(1000)
    assert j > 0 and c > 0

@task("4 Point slots")
def _():
    p = tasks.Point()
    p.x, p.y = 1, 2
    try:
        p.z = 3
    except AttributeError:
        pass
    else:
        raise AssertionError("__slots__ should block new attributes")

@task("5 run_max_times")
def _():
    @tasks.run_max_times(2)
    def ping():
        return "pong"
    assert ping() == ping() == "pong"
    try:
        ping()
    except RuntimeError:
        pass
    else:
        raise AssertionError("third call should raise RuntimeError")

@task("6 lazy log filtering")
def _():
    p = os.path.join(tempfile.mkdtemp(), "app.log")
    open(p, "w").write("INFO start\nERROR tuner lost\nWARN gain\nERROR overflow\n")
    g = tasks.read_large_file(p)
    assert inspect.isgenerator(g) and next(g) == "INFO start"
    e = tasks.error_lines(p)
    assert inspect.isgenerator(e) and list(e) == ["ERROR tuner lost", "ERROR overflow"]

@task("7 Pixel slots")
def _():
    px = [tasks.Pixel(i, 0, 0) for i in range(1000)]
    assert tasks.sum_red(px) == 499500 and not hasattr(px[0], "__dict__")
    assert tasks.slots_saves_memory() is True

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
