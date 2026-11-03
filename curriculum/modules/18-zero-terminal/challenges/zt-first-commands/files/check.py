#!/usr/bin/env python3
"""Run with ./check. Tests each task in the files you create in this folder and lists what still fails."""
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

import pwd

@task("1 hello.txt")
def _():
    got = text("hello.txt").strip()
    assert got.lower() == "hello terminal" or got == "Hello terminal", f"hello.txt contains {got!r}, it should contain Hello terminal. Use echo with the text, then > and the file name"
    assert got == "Hello terminal", f"hello.txt contains {got!r}. Capital letters matter: it should be exactly Hello terminal (capital H, small t)"

@task("2 me.txt")
def _():
    got = text("me.txt").strip()
    assert got, "me.txt is empty. Put whoami in front of the >, so its output goes into the file"
    # ponytail: any real account name passes; checking the exact creator is not worth the complexity.
    try:
        pwd.getpwnam(got)
    except KeyError:
        raise AssertionError(f"me.txt contains {got!r}, which is not a user name on this computer. Do not type your name yourself. Let whoami write it into the file with >")

@task("3 today.txt")
def _():
    got = text("today.txt")
    assert re.search(r"\b(19|20)\d\d\b", got) and re.search(r"\d{1,2}:\d\d", got), f"today.txt contains {got.strip()!r}, which does not look like the output of date. Put date in front of the >"

@task("4 list.txt with two lines")
def _():
    got = lines_of(text("list.txt"))
    assert got != ["second"], "list.txt only has the line second. The > in your second command replaced the file. Use > for first, then >> for second"
    assert got == ["first", "second"], f"list.txt has these lines: {got}. It should have exactly two lines: first, then second. Start over: make the file with > and the first line, then add the second line with >>"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
