#!/usr/bin/env python3
"""Run with ./check. Tests each task in answers/task1.sh to answers/task8.sh and lists what still fails."""
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
RNG = random.Random(107)


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

TREE = {'challenge/read_me': 'academy{practice_readfile}\n'}
PROGS = {'challenge/run': '#!/bin/bash\necho "PWN=${PWN-<unset>}"\necho "COLLEGE=${COLLEGE-<unset>}"\n', 'challenge/secret': '#!/bin/bash\necho "@SECRET@"\n'}
PRACTICE = {'@SECRET@': 'academy{practice_subst}'}


def sourced(n, root, names, stdin=None, env=None):
    """Source the answer in bash, then report the variables in `names` as the shell sees them."""
    home = root / "home/hacker"
    tail = "".join(f'; printf "VAR {v}=%s\\n" "${{{v}-<unset>}}"' for v in names)
    e = {**os.environ, "DOJO": str(root), "HOME": str(home), **(env or {})}
    r = subprocess.run(["bash", "-c", 'source "$0"' + tail, str(answer(n))], cwd=home,
                       input=stdin or "", env=e, capture_output=True, text=True, timeout=20)
    vals = dict(l[4:].split("=", 1) for l in r.stdout.splitlines() if l.startswith("VAR "))
    return r, vals

@task("1 printing variables")
def _():
    v = secret("echo")
    r, _ = go(1, dojo(), env={"FLAG": v})
    assert r.stdout.strip() == v, f"print the value of the FLAG variable {show(r)}"

@task("2 setting variables")
def _():
    r, vals = sourced(2, dojo(), ["PWN"])
    assert vals.get("PWN") == "COLLEGE", f"PWN is {vals.get('PWN')!r}. It should be COLLEGE (no spaces around =) {show(r)}"

@task("3 multi-word variables")
def _():
    r, vals = sourced(3, dojo(), ["PWN"])
    assert vals.get("PWN") == "COLLEGE YEAH", f"PWN is {vals.get('PWN')!r}. It should be 'COLLEGE YEAH' (put it in quotes) {show(r)}"

@task("4 exporting variables")
def _():
    r, vals = sourced(4, dojo(), ["COLLEGE"])
    assert "PWN=COLLEGE" in r.stdout.splitlines(), f"run must see PWN=COLLEGE, so export it {show(r)}"
    assert "COLLEGE=<unset>" in r.stdout.splitlines(), f"run must NOT see COLLEGE, so set it without export {show(r)}"
    assert vals.get("COLLEGE") == "PWN", f"COLLEGE is {vals.get('COLLEGE')!r} in your shell. It should be PWN"

@task("5 printing exported variables")
def _():
    v = secret("env")
    env = {"FLAG": v, "FLAGPOLE": secret("decoy"), "NOT_FLAG": secret("decoy"), "MYFLAG": secret("decoy")}
    r, _ = go(5, dojo(), env=env)
    assert r.stdout.strip() == f"FLAG={v}", f"print only the FLAG=... line of env {show(r)}"

@task("6 storing command output")
def _():
    s = secret("subst")
    r, vals = sourced(6, dojo(subs={"@SECRET@": s}), ["PWN"])
    assert vals.get("PWN") == s, f"PWN should hold the output of $DOJO/challenge/secret. It is {vals.get('PWN')!r} {show(r)}"

@task("7 reading input")
def _():
    typed = word()  # a new line each run, so only read can know it
    r, vals = sourced(7, dojo(), ["PWN"], stdin=typed + "\n")
    assert vals.get("PWN") == typed, f"use read to set PWN from the input line. PWN is {vals.get('PWN')!r} {show(r)}"

@task("8 reading files")
def _():
    s = secret("readfile")
    r, vals = sourced(8, dojo({"challenge/read_me": s + "\n"}), ["PWN"])
    assert vals.get("PWN") == s, f"read $DOJO/challenge/read_me into PWN. PWN is {vals.get('PWN')!r} {show(r)}"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
