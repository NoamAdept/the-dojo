#!/usr/bin/env python3
"""Run with ./check. Tests each task in answers/task1.sh to answers/task4.sh and lists what still fails."""
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

def out(r):
    return f"(your script printed {r.stdout.strip()!r}" + (f", and this error: {r.stderr.strip()!r})" if r.stderr.strip() else ")")

@task("1 print a line")
def _():
    r, _ = run(1)
    assert r.stdout.strip() == "hello from my script", f"task1.sh should print hello from my script {out(r)}"

@task("2 three lines")
def _():
    r, _ = run(2)
    got = r.stdout.split()
    assert got == ["ready", "steady", "go"], f"task2.sh should print ready, steady and go on three lines {out(r)}"
    assert r.stdout.strip().splitlines() == ["ready", "steady", "go"], "put each word on its own line with its own echo"

@task("3 make result.txt")
def _():
    r, cwd = run(3)
    f = cwd / "result.txt"
    assert f.is_file(), f"after running task3.sh there was no result.txt in the folder it ran in. The script itself must create it, e.g. with echo and > {out(r)}"
    got = f.read_text().strip()
    assert got == "made by a script", f"result.txt contains {got!r}, it should contain made by a script"

@task("4 box/note.txt")
def _():
    r, cwd = run(4)
    assert (cwd / "box").is_dir(), f"after running task4.sh there was no folder box. The script must make the folder first, with mkdir {out(r)}"
    f = cwd / "box" / "note.txt"
    assert f.is_file(), f"there is a folder box, but no note.txt inside it. Add a second line that writes into box/note.txt {out(r)}"
    got = f.read_text().strip()
    assert got == "inside", f"box/note.txt contains {got!r}, it should contain inside"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
