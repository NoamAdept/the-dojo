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
rng = random.Random(8)
tmp = tempfile.mkdtemp()

def tmpfile(name, text):
    p = os.path.join(tmp, name)
    with open(p, "w") as f:
        f.write(text)
    return p

@task("1 read_all")
def _():
    text = "".join(f"line {rng.randint(0, 999)}\n" for _ in range(4))
    same(tasks.read_all(tmpfile("a.txt", text)), text, "read_all on a 4-line file")

@task("2 count_lines")
def _():
    n = rng.randint(3, 12)
    p = tmpfile("b.txt", "".join(f"{i}\n" for i in range(n)))
    same(tasks.count_lines(p), n, f"count_lines on a {n}-line file")
    same(tasks.count_lines(tmpfile("e.txt", "")), 0, "count_lines on an empty file")

@task("3 read_lines")
def _():
    p = tmpfile("c.txt", "# header\nalpha 3\n\n  bravo 4  \n#note\necho 1\n")
    same(tasks.read_lines(p), ["alpha 3", "bravo 4", "echo 1"], "read_lines on a file with # comments, a blank line and extra spaces")

@task("4 write_lines")
def _():
    p = os.path.join(tmp, "out.txt")
    lines = [f"line {rng.randint(0, 999)}" for _ in range(3)]
    tasks.write_lines(p, lines)
    assert os.path.exists(p), "write_lines did not create the file. Open it with open(path, \"w\")"
    text = open(p).read()
    want = "".join(l + "\n" for l in lines)
    assert text == want, f"the file holds {text!r}, but it should hold {want!r}. Write each line, then \"\\n\""

@task("5 shout_file")
def _():
    src = tmpfile("s.txt", "# skip me\nfm radio\n\nPi beacon\n")
    dst = os.path.join(tmp, "loud.txt")
    tasks.shout_file(src, dst)
    assert os.path.exists(dst), "shout_file did not create the output file dst"
    got = open(dst).read()
    assert got == "FM RADIO\nPI BEACON\n", f"the output file holds {got!r}, but it should hold 'FM RADIO\\nPI BEACON\\n'"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
