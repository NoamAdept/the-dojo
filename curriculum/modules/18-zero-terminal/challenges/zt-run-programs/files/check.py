#!/usr/bin/env python3
"""Run with ./check. Tests each task in greet.txt, locked.txt, data/settings.txt, report.txt and config.txt and lists what still fails."""
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

import os, re

def text(name):
    """Contents of a file in this folder, or a plain-English error if it is missing."""
    if os.path.isdir(name):
        raise AssertionError(f"{name} is a folder, but it should be a file")
    if not os.path.isfile(name):
        raise AssertionError(f"there is no file named {name} in this folder yet")
    return open(name, errors="replace").read()

def lines_of(s):
    """Lines without trailing spaces, ignoring empty lines at the very end."""
    return [x.rstrip() for x in s.rstrip().splitlines()]

import subprocess

@task("1 greet.txt")
def _():
    got = text("greet.txt").strip()
    assert got == "Hello! Your code is 42-beacon", f"greet.txt contains {got!r}. It should hold what ./greet prints. Run it with ./ in front and send its output into greet.txt with >"

@task("2 locked.txt")
def _():
    if not os.path.exists("locked.txt") and not os.access("locked", os.X_OK):
        raise AssertionError("locked is not executable yet. Give it the execute permission with chmod, then save its output into locked.txt")
    got = text("locked.txt").strip()
    assert got == "unlocked: 5150-door", f"locked.txt contains {got!r}. It should hold what ./locked prints once it is allowed to run. Save its output with >"

@task("3 data/settings.txt and report.txt")
def _():
    assert os.path.isdir("data"), "there is no folder data yet. Make it with mkdir"
    s = text("data/settings.txt").strip()
    assert s == "volume=7", f"data/settings.txt contains {s!r}, it should contain exactly volume=7"
    got = text("report.txt").strip()
    assert got == "report ready, settings: volume=7", f"report.txt contains {got!r}. After making data/settings.txt, run ./report again and save its output into report.txt"

@task("4 config.txt")
def _():
    r = subprocess.run(["bash", "checkme"], capture_output=True, text=True, timeout=10)
    assert "ALL GOOD" in r.stdout, "./checkme still finds a problem: " + (r.stdout + r.stderr).strip()
    got = lines_of(text("config.txt"))
    assert got[:2] == ["name=pi-radio", "band=fm"] and len(got) >= 3 and re.fullmatch(r"gain=[0-9]+", got[2]), \
        f"config.txt is {got}; run ./checkme and fix what it says"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
