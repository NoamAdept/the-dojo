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

import contextlib, io, os, tempfile, time, tasks

@task("1 write_numbers")
def _():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "numbers.txt")
        tasks.write_numbers(p)
        assert open(p).read().split() == [str(i) for i in range(1, 11)]

@task("2 html_tag")
def _():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            with tasks.html_tag("b"):
                print("x")
                raise KeyError
        except KeyError:
            pass
    assert buf.getvalue().split() == ["<b>", "x", "</b>"], buf.getvalue()

@task("3 ExceptionSpy re-raises")
def _():
    spy = tasks.ExceptionSpy()
    try:
        with contextlib.redirect_stdout(io.StringIO()), spy:
            raise ValueError("boom")
    except ValueError:
        pass
    else:
        raise AssertionError("the exception must propagate")
    assert spy.seen is True

@task("4 temp dir lifecycle")
def _():
    assert tasks.temp_dir_lifecycle() == (True, False)

@task("5 Timer and time_it")
def _():
    with tasks.Timer() as t:
        time.sleep(0.05)
    assert 0.04 < t.elapsed < 1
    @tasks.time_it
    def nap():
        time.sleep(0.02)
        return "ok"
    assert nap() == "ok" and 0.015 < nap.last_elapsed < 1

@task("6 DatabaseConnection")
def _():
    log = []
    with tasks.DatabaseConnection(log) as cur:
        assert cur.execute("SELECT 1") == "ran: SELECT 1"
    assert log == ["connect", "commit", "disconnect"], log
    log.clear()
    try:
        with tasks.DatabaseConnection(log):
            raise RuntimeError
    except RuntimeError:
        pass
    else:
        raise AssertionError("don't swallow exceptions")
    assert log == ["connect", "rollback", "disconnect"], log

@task("7 Indenter")
def _():
    with tasks.Indenter():
        assert tasks.indented("L1") == "    L1"
        with tasks.Indenter():
            assert tasks.indented("L2") == "        L2"
        assert tasks.indented("L1") == "    L1"
    assert tasks.indented("L0") == "L0"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
