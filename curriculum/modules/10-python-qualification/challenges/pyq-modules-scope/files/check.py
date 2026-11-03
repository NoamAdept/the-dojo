#!/usr/bin/env python3
"""Run with ./check. Tests each task in tasks.py and config_pkg/ and lists what still fails."""
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

import importlib, os, tasks

@task("1 factorial_of_ten")
def _():
    assert tasks.factorial_of_ten() == 3628800

@task("2 current_dir")
def _():
    assert tasks.current_dir() == os.getcwd()
    import ast
    imports = [(a.name, a.asname) for n in ast.walk(ast.parse(open("tasks.py").read()))
               if isinstance(n, ast.Import) for a in n.names]
    assert ("os", "operating_system") in imports, "import os as operating_system"

@task("3 increment uses global")
def _():
    tasks.score = 5
    tasks.increment()
    assert tasks.score == 6, f"score is {tasks.score}, expected 6"

@task("4 maker closure")
def _():
    f10 = tasks.maker(10)
    assert f10(5) == 15 and tasks.maker(-1)(1) == 0
    assert f10.__closure__, "the inner function should keep n in its closure"

@task("5 simple_calc module")
def _():
    calc = importlib.import_module("simple_calc")
    assert calc.add(4, 5) == 9 and calc.sub(4, 5) == -1
    assert tasks.calc_demo() == (5, 6)

@task("6 config_pkg re-exports DEFAULT_CONFIG")
def _():
    assert os.path.isfile("config_pkg/__init__.py") and os.path.isfile("config_pkg/settings.py")
    pkg = importlib.import_module("config_pkg")
    settings = importlib.import_module("config_pkg.settings")
    assert pkg.DEFAULT_CONFIG is settings.DEFAULT_CONFIG and "sample_rate" in pkg.DEFAULT_CONFIG

@task("7 decorator registry")
def _():
    assert len(tasks.REGISTRY) >= 3, "decorate at least three functions"
    def extra():
        return "extra"
    assert tasks.register(extra) is extra and tasks.REGISTRY["extra"] is extra
    results = tasks.run_all()
    assert set(results) == set(tasks.REGISTRY) and results["extra"] == "extra"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
