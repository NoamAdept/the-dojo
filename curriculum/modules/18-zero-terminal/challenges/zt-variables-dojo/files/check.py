#!/usr/bin/env python3
"""Run with ./check. Tests each task in answers/task1.sh to answers/task5.sh and lists what still fails."""
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
RNG = random.Random(1806)

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

@task("1 print HOME")
def _():
    root = dojo()
    r = go(1, root)
    assert r.stdout.strip() == str(root / "home/hacker"), f"task1.sh should print the value of HOME. Put a $ in front of a variable name to get its value {show(r)}"

@task("2 your own variable")
def _():
    r = go(2, dojo())
    assert r.stdout.strip() == "listening on fm", f"task2.sh should print listening on fm {show(r)}"
    src = answer(2).read_text()
    m = re.search(r"""(?:^|[\s;])band=("fm"|'fm'|fm)(?=$|[\s;])""", src, re.M)
    assert m, "set the variable with band=fm (no spaces around =)"
    # Give band another value: the output must follow it, so it really comes from $band.
    other = word()
    alt = sandbox({"task2.sh": src[:m.start(1)] + other + src[m.end(1):]}) / "task2.sh"
    root = dojo()
    home = root / "home/hacker"
    r2 = subprocess.run(["bash", str(alt)], cwd=home, env={**os.environ, "DOJO": str(root), "HOME": str(home)},
                        capture_output=True, text=True, timeout=20)
    assert r2.stdout.strip() == f"listening on {other}", "print the value with $band. Do not type fm a second time"

@task("3 read $DOJO/message.txt")
def _():
    msg = f"secret message {word()}"
    r = go(3, dojo({"message.txt": msg + "\n"}))
    assert r.stdout.strip() == msg, f"task3.sh should print the contents of $DOJO/message.txt. Build the path from the DOJO variable, and do not type the practice text {show(r)}"

@task("4 write $DOJO/tmp/finished.txt")
def _():
    root = dojo()
    r = go(4, root)
    f = root / "tmp/finished.txt"
    assert f.is_file(), f"after task4.sh there was no $DOJO/tmp/finished.txt. Build the path from the DOJO variable, and write the file with echo and > {show(r)}"
    assert f.read_text().strip() == "done", f"finished.txt contains {f.read_text().strip()!r}, it should contain done"

@task("5 a path with a space")
def _():
    note = f"notes {word()}"
    r = go(5, dojo({"my notes/today.txt": note + "\n"}))
    assert r.stdout.strip() == note, f"task5.sh should print $DOJO/my notes/today.txt. The path has a space in it: put the whole path in double quotes, so the shell keeps it as one word {show(r)}"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
