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

def assigned(name):
    """The expression of the last top-level `name = ...` line in tasks.py."""
    import ast
    found = None
    for node in ast.parse(open("tasks.py").read()).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            found = node.value
    return found

def again(name, **values):
    """Work out `name` again with other starting values, to prove it uses the variables."""
    import ast
    expr = ast.Expression(assigned(name))
    return eval(compile(expr, "tasks.py", "eval"), {**vars(tasks), **values})

def filled(name):
    v = getattr(tasks, name, None)
    if v is None:
        raise NotImplementedError
    return v

@task("1 station is a str")
def _():
    v = filled("station")
    assert isinstance(v, str), f"station is a {type(v).__name__}; put the text in quotes to make a str"
    assert v == "Pi Radio", f"station is {v!r}; it should be 'Pi Radio' (capital P and R, one space)"

@task("2 channels is an int")
def _():
    v = filled("channels")
    assert type(v) is int, f"channels is a {type(v).__name__}; write 16 with no quotes and no decimal point"
    assert v == 16, f"channels is {v}; it should be 16"

@task("3 gain_db is a float")
def _():
    v = filled("gain_db")
    assert type(v) is float, f"gain_db is a {type(v).__name__}; write 20.5 with no quotes"
    assert v == 20.5, f"gain_db is {v}; it should be 20.5"

@task("4 is_on is a bool")
def _():
    v = filled("is_on")
    assert type(v) is bool, f"is_on is a {type(v).__name__}; write True with a capital T and no quotes"
    assert v is True, "is_on should be True"

@task("5 as_int converts the text")
def _():
    v = filled("as_int")
    assert type(v) is int, f"as_int is a {type(v).__name__}; use int(text_number)"
    assert v == 433, f"as_int is {v}; it should be 433"
    assert again("as_int", text_number="1234") == 1234, "make as_int with int(text_number), so it converts the variable instead of typing 433"

@task("6 label is built with an f-string")
def _():
    v = filled("label")
    assert v == "Pi Radio has 16 channels", f"label is {v!r}; it should be 'Pi Radio has 16 channels'"
    import ast
    hint = "build label with an f-string: f\"{station} has {channels} channels\""
    assert isinstance(assigned("label"), ast.JoinedStr), hint
    assert again("label", station="Moon Base", channels=3) == "Moon Base has 3 channels", hint

@task("7 pi_text has two decimals")
def _():
    v = filled("pi_text")
    assert v == "3.14", f"pi_text is {v!r}; it should be the string '3.14'"
    import ast
    hint = "make pi_text with f\"{pi:.2f}\" so Python does the rounding"
    assert isinstance(assigned("pi_text"), ast.JoinedStr), hint
    assert again("pi_text", pi=2.71828) == "2.72", hint

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
