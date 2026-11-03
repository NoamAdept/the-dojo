#!/usr/bin/env python3
"""Run with ./check. Tests each task in answers/task1.sh to answers/task3.sh and stopped.txt and lists what still fails."""
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

import os, pathlib, shutil, subprocess, tempfile

HERE = pathlib.Path(".").resolve()

def answer(n):
    """Path of answers/taskN.sh; NotImplementedError while it still says TODO."""
    p = HERE / "answers" / f"task{n}.sh"
    if not p.exists() or "TODO" in p.read_text():
        raise NotImplementedError
    return p

def sandbox(files=None):
    """Fresh temp dir filled with {relative path: text or bytes}. Returns its Path."""
    # ponytail: sandboxes live in /tmp and are left for the OS to clean.
    d = pathlib.Path(tempfile.mkdtemp(prefix="academy-sh-"))
    for rel, data in (files or {}).items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data) if isinstance(data, bytes) else p.write_text(data)
    return d

def run(n, cwd=None, stdin=None, env=None, args=(), timeout=20):
    """Run answers/taskN.sh with bash in cwd (a new sandbox by default).
    Returns (CompletedProcess, cwd). HOME points at the sandbox unless env overrides it."""
    cwd = cwd or sandbox()
    e = {**os.environ, "HOME": str(cwd), **(env or {})}
    r = subprocess.run(["bash", str(answer(n)), *args], cwd=cwd, input=stdin, env=e,
                       capture_output=True, text=True, timeout=timeout)
    return r, cwd

import random, re
RNG = random.Random(1807)

def word(n=8):
    return "".join(RNG.choice("abcdefghjkmnpqrstuvwxyz23456789") for _ in range(n))

def dojo(files=None):
    """Fresh fake filesystem with home/hacker and tmp. Returns its Path."""
    root = sandbox(files).resolve()
    for d in ("home/hacker", "tmp"):
        (root / d).mkdir(parents=True, exist_ok=True)
    return root

def go(n, root):
    """Run answers/taskN.sh from $HOME with DOJO and HOME set, like ./try does."""
    home = root / "home/hacker"
    r, _ = run(n, cwd=home, env={"DOJO": str(root), "HOME": str(home)})
    return r

def show(r):
    return f"(your script printed: {r.stdout[-300:]!r}, errors: {r.stderr[-300:]!r})"

import time
LONG = 'a-really-long-file-name-made-for-tab-completion-q7.txt'

@task("1 count lines")
def _():
    n = RNG.randint(40, 90)
    root = dojo({"log.txt": "".join(f"line {i}: level {RNG.randint(1, 99)}\n" for i in range(1, n + 1))})
    r = go(1, root)
    rest = r.stdout.replace(str(root / "log.txt"), "").replace("log.txt", "")
    nums = re.findall(r"\d+", rest)
    assert nums, f"task1.sh should print the number of lines in $DOJO/log.txt, with wc and the option for lines {show(r)}"
    assert nums == [str(n)], f"task1.sh printed {nums}, but the file has {n} lines. Plain wc prints three numbers (lines, words, bytes); find the option for lines only in wc --help {show(r)}"

@task("2 just the year")
def _():
    r = go(2, dojo())
    year = time.strftime("%Y")
    assert r.stdout.strip() == year, f"task2.sh should print only {year}. Look in date --help for the piece that means year, and use date +PIECE {show(r)}"

@task("3 the long file name")
def _():
    msg = f"you typed it right {word()}"
    r = go(3, dojo({"signals/" + LONG: msg + "\n"}))
    assert r.stdout.strip() == msg, f"task3.sh should print the contents of $DOJO/signals/{LONG}. Check the name carefully (Tab completion helps) {show(r)}"

@task("4 stopped twice with Ctrl-C")
def _():
    if not os.path.exists("stopped.txt"):
        raise AssertionError("there is no stopped.txt yet. Run ./forever and press Ctrl-C to stop it")
    n = sum(1 for x in open("stopped.txt") if "stopped with Ctrl-C" in x)
    assert n >= 2, f"you stopped ./forever {n} time(s). Press the up arrow and Enter to run it again, then Ctrl-C once more"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
