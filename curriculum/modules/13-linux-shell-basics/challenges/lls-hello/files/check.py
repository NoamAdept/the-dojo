#!/usr/bin/env python3
"""Run with ./check. Tests each task in answers/task1.sh to answers/task3.sh and lists what still fails."""
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
RNG = random.Random(101)


def word(n=8):
    return "".join(RNG.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(n))


def secret(tag="s"):
    return "academy{%s_%s}" % (tag, word(12))


def dojo(tree=None, subs=None):
    """Fresh fake root from TREE and PROGS (plus overrides). Returns its resolved Path."""
    root = sandbox({**TREE, **(tree or {})}).resolve()
    for d in ("home/hacker", "tmp"):
        (root / d).mkdir(parents=True, exist_ok=True)
    allsubs = {**PRACTICE, **(subs or {})}
    for rel, body in PROGS.items():
        for k, v in allsubs.items():
            body = body.replace(k, v)
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body)
        p.chmod(0o755)
    return root


def go(n, root, cwd=None, stdin=None, env=None, timeout=20):
    """Run answers/taskN.sh the way the README describes. Returns (result, token)."""
    home = root / "home/hacker"
    tok = word()
    e = {"DOJO": str(root), "HOME": str(home), "TOKEN": tok,
         "PATH": str(root / "bin") + os.pathsep + os.environ.get("PATH", ""), **(env or {})}
    r, _ = run(n, cwd=cwd or home, stdin=stdin, env=e, timeout=timeout)
    return r, tok


def show(r):
    return f"(stdout: {r.stdout[-300:]!r}, stderr: {r.stderr[-300:]!r})"


def reports(r, tok):
    """Each run of a reporting program whose token matches: dict(argv0, cwd, args)."""
    out, cur = [], None
    for line in r.stdout.splitlines():
        if line.startswith("RAN argv0="):
            cur = {"argv0": line[10:], "args": []}
        elif cur is not None and line.startswith("RAN cwd="):
            cur["cwd"] = line[8:]
        elif cur is not None and line.startswith("RAN arg="):
            cur["args"].append(line[8:])
        elif cur is not None and line.startswith("RAN token="):
            if line[10:] == tok:
                out.append(cur)
            cur = None
    return out


def report(r, tok, prog="the challenge program"):
    reps = reports(r, tok)
    assert reps, f"{prog} never ran {show(r)}"
    return reps[-1]


def lines(r):
    return [x for x in r.stdout.splitlines() if x.strip()]

TREE = {'home/hacker/.bash_history': 'ls\ncd /tmp\ncat notes.txt\nwhoami\necho hi there\nls -l\npwd\ncd ~\ndate\nuname -a\necho academy{practice_history}\n'}
PROGS = {'bin/hello': '#!/bin/bash\nif [ $# -eq 0 ]; then\n    echo "Hello! You just ran your first command."\n    echo "TOKEN ${TOKEN:-practice}"\nelif [ $# -eq 1 ] && [ "$1" = hackers ]; then\n    echo "Hello, hackers! You passed exactly one argument."\n    echo "ARG-TOKEN ${TOKEN:-practice}"\nelse\n    echo "hello: give me no arguments, or exactly one argument: hackers (you gave $#: $*)" >&2\n    exit 1\nfi\n'}
PRACTICE = {}


@task("1 run the hello command")
def _():
    r, tok = go(1, dojo())
    assert f"TOKEN {tok}" in r.stdout.splitlines(), f"run `hello` with no arguments {show(r)}"

@task("2 hello with one argument")
def _():
    r, tok = go(2, dojo())
    assert f"ARG-TOKEN {tok}" in r.stdout.splitlines(), f"run `hello hackers` (lowercase, one argument) {show(r)}"

@task("3 most recent history entry")
def _():
    hist = [RNG.choice(["ls", "pwd", "whoami", "date", "cd /tmp", "cat " + word(5) + ".txt"]) for _ in range(40)]
    hist.append("echo " + secret("history"))
    r, _ = go(3, dojo({"home/hacker/.bash_history": "\n".join(hist) + "\n"}))
    assert r.stdout.strip() == hist[-1], f"print only the last line of ~/.bash_history. Expected {hist[-1]!r} {show(r)}"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
