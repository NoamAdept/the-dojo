#!/usr/bin/env python3
"""Run with ./check. Tests each task in shopping.txt, poem.txt, code.txt and both.txt and lists what still fails."""
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

POEM_FIXED = ['Night falls on the hill', 'The radio hums softly', 'A signal from far away', 'Says hello']
CODE = 'violet-6666'

@task("1 shopping.txt")
def _():
    got = [x.strip() for x in lines_of(text("shopping.txt")) if x.strip()]
    assert got == ["antenna", "cable", "battery"], f"shopping.txt has these lines: {got}. It should have exactly antenna, cable, battery, each on its own line, in that order"

@task("2 poem.txt typo fixed")
def _():
    got = lines_of(text("poem.txt"))
    assert "radoi" not in " ".join(got), "poem.txt still says radoi in line 2. Open it with vim poem.txt, fix it to radio, then press Esc and type :wq"
    assert got == POEM_FIXED, f"poem.txt should be exactly these lines: {POEM_FIXED}, but it is {got}. Fix only the typo and change nothing else"

@task("3 code.txt")
def _():
    got = text("code.txt").strip()
    assert got == CODE, f"code.txt contains {got!r}. Read message.txt with cat message.txt and copy the code word exactly"

@task("4 both.txt")
def _():
    want = text("shopping.txt") + text("poem.txt")
    got = text("both.txt")
    assert lines_of(got) == lines_of(want), "both.txt should hold shopping.txt and then poem.txt (as they are now). Make it again with cat, the 2 file names in that order, and >"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
