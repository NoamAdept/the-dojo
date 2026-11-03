#!/usr/bin/env python3
"""Run with ./check. Tests each task in the folders and files you create in this folder and lists what still fails."""
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

import pathlib

@task("1 radio folder")
def _():
    assert os.path.isdir("radio"), "there is no folder named radio here yet. Make one with mkdir"

@task("2 radio/notes folder")
def _():
    assert os.path.isdir("radio/notes"), "there is no folder notes inside radio yet. mkdir can make a folder inside another one when you give it the path"

@task("3 here.txt from pwd")
def _():
    if not os.path.exists("radio/notes/here.txt") and os.path.exists("here.txt"):
        raise AssertionError("here.txt is in the challenge folder, but it should be inside radio/notes. cd into radio/notes first, then save the output of pwd there")
    got = text("radio/notes/here.txt").strip()
    assert got.startswith("/"), f"radio/notes/here.txt contains {got!r}. It should hold the output of pwd, which starts with /"
    assert got.endswith("/radio/notes"), f"radio/notes/here.txt contains {got!r}. Run pwd while you are standing inside radio/notes"

@task("4 maze-list.txt")
def _():
    want = sorted(os.listdir("maze"))
    got = lines_of(text("maze-list.txt"))
    if len(got) == 1:
        got = got[0].split()
    assert got == want, f"maze-list.txt contains {got}, but ls maze lists {want}. From the challenge folder, save the output of ls maze into maze-list.txt with >"

@task("5 key.txt")
def _():
    keys = [p.name for p in pathlib.Path("maze").glob("*/*/*/key-*")]
    assert keys, "the key file in maze is gone. If you deleted something by accident, restart the challenge"
    got = os.path.basename(text("key.txt").strip())  # the bare name, or its path inside maze
    assert got.startswith("key-"), f"key.txt contains {got!r}. It should hold the name of the file that starts with key-"
    assert got == keys[0], f"key.txt contains {got!r}, which is not the right key. Look again, the name must match exactly"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
