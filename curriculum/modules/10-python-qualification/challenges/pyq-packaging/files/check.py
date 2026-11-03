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

import os, tempfile, tasks
from pathlib import Path

@task("1 project_name")
def _():
    assert tasks.project_name("demo_project/pyproject.toml") == "pi-receiver"

@task("2 can_import")
def _():
    assert tasks.can_import("json") is True and tasks.can_import("no_such_module_xyz") is False

@task("3 is_installed")
def _():
    assert tasks.is_installed("json") is True and tasks.is_installed("no_such_module_xyz") is False

@task("4 remove_tree")
def _():
    d = Path(tempfile.mkdtemp()) / "x"
    (d / "y").mkdir(parents=True)
    tasks.remove_tree(d)
    assert not d.exists()
    tasks.remove_tree(d)  # already gone: no error

@task("5 scaffold")
def _():
    with tempfile.TemporaryDirectory() as root:
        tasks.scaffold(root, "radio")
        r = Path(root)
        assert (r / "src/radio/__init__.py").is_file() and (r / "tests").is_dir()
        assert "radio" in (r / "README.md").read_text()

@task("6 parse_requirements")
def _():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "requirements.txt"
        p.write_text("# deps\nnumpy==1.26.4\n\nscipy>=1.10\nrequests[socks]~=2.31 ; python_version>'3.8'\nuhd\n")
        assert tasks.parse_requirements(p) == ["numpy", "scipy", "requests", "uhd"]

@task("7 VirtualEnv")
def _():
    with tempfile.TemporaryDirectory() as d:
        env = tasks.VirtualEnv(os.path.join(d, ".venv"))
        env.create()
        assert Path(env.python).exists()
        script = Path(d) / "hi.py"
        script.write_text("import sys; print(sys.prefix)")
        assert ".venv" in env.run_script(script)

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
