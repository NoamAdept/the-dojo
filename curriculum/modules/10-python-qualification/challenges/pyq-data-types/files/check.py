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

import tasks, typing

@task("1 slicing")
def _():
    assert tasks.extract_program("PythonProgramming") == "Program"

@task("2 f-string")
def _():
    assert tasks.format_item("Apples", 2.5) == "Item: Apples | Cost: $2.50"
    assert tasks.format_item("Pi", 35) == "Item: Pi | Cost: $35.00"

@task("3 safe_div")
def _():
    assert tasks.safe_div(7, 2) == 3.5
    assert tasks.safe_div(1, 0) is None
    assert tasks.safe_div("4", 2) is None and tasks.safe_div(True, 1) is None

@task("4 type hints on power")
def _():
    hints = typing.get_type_hints(tasks.power)
    assert hints == {"base": float, "exp": float, "return": float}, f"hints are {hints}"

@task("5 palindrome")
def _():
    assert tasks.is_palindrome("Race Car") and tasks.is_palindrome("a")
    assert not tasks.is_palindrome("radio")

@task("6 clean_numbers")
def _():
    out = tasks.clean_numbers(["10", "2.5", "invalid", 5, 20.0, None])
    assert out == [10.0, 2.5, 5.0, 20.0] and all(type(x) is float for x in out)

@task("7 HexNumber")
def _():
    h = tasks.HexNumber("0xA")
    assert int(h) == 10 and str(h) == "0xa"
    assert int(tasks.HexNumber("0XFF")) == 255

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
