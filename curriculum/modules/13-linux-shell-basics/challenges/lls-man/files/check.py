#!/usr/bin/env python3
"""Run with ./check. Tests each task in answers/task1.sh to answers/task7.sh and lists what still fails."""
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
RNG = random.Random(104)


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

TREE = {'flag': 'academy{practice_printfile}\n', 'usr/share/man/man1/challenge.1': '.TH CHALLENGE 1 "2026" "Academy" "Academy Manual"\n.SH NAME\nchallenge \\- a program that rewards people who read manuals\n.SH SYNOPSIS\n.B challenge\n[\\fIOPTION\\fR]\n.SH DESCRIPTION\n.B challenge\ndoes nothing useful unless you give it the right option.\n.TP\n.B --giveflag\nprint the giveflag success message\n.TP\n.BI --printfile " PATH"\nprint the file at PATH\n.TP\n.B --sesame\nprint the manual success message\n.SH SEE ALSO\nman(1)\n', 'usr/share/man/man1/challenge-full.1': '.TH CHALLENGE-FULL 1 "2026" "Academy" "Academy Manual"\n.SH NAME\nchallenge-full \\- every option of challenge\n.SH DESCRIPTION\nchallenge accepts many options. Exactly one prints the search success message.\n.TP\n.B --adjust-0\nadjust the signal using method 0; this does not print any success message\n.TP\n.B --balance-1\nbalance the signal using method 1; this does not print any success message\n.TP\n.B --calibrate-2\ncalibrate the signal using method 2; this does not print any success message\n.TP\n.B --decimate-3\ndecimate the signal using method 3; this does not print any success message\n.TP\n.B --equalize-4\nequalize the signal using method 4; this does not print any success message\n.TP\n.B --filter-5\nfilter the signal using method 5; this does not print any success message\n.TP\n.B --gate-6\ngate the signal using method 6; this does not print any success message\n.TP\n.B --heterodyne-7\nheterodyne the signal using method 7; this does not print any success message\n.TP\n.B --integrate-8\nintegrate the signal using method 8; this does not print any success message\n.TP\n.B --jitter-9\njitter the signal using method 9; this does not print any success message\n.TP\n.B --key-10\nkey the signal using method 10; this does not print any success message\n.TP\n.B --limit-11\nlimit the signal using method 11; this does not print any success message\n.TP\n.B --modulate-12\nmodulate the signal using method 12; this does not print any success message\n.TP\n.B --normalize-13\nnormalize the signal using method 13; this does not print any success message\n.TP\n.B --oversample-14\noversample the signal using method 14; this does not print any success message\n.TP\n.B --pan-15\npan the signal using method 15; this does not print any success message\n.TP\n.B --quantize-16\nquantize the signal using method 16; this does not print any success message\n.TP\n.B --resample-17\nresample the signal using method 17; this does not print any success message\n.TP\n.B --squelch-18\nsquelch the signal using method 18; this does not print any success message\n.TP\n.B --tune-19\ntune the signal using method 19; this does not print any success message\n.TP\n.B --unwrap-20\nunwrap the signal using method 20; this does not print any success message\n.TP\n.B --vary-21\nvary the signal using method 21; this does not print any success message\n.TP\n.B --window-22\nwindow the signal using method 22; this does not print any success message\n.TP\n.B --xfade-23\nxfade the signal using method 23; this does not print any success message\n.TP\n.B --yield-24\nyield the signal using method 24; this does not print any success message\n.TP\n.B --zero-25\nzero the signal using method 25; this does not print any success message\n.TP\n.B --adjust-26\nadjust the signal using method 26; this does not print any success message\n.TP\n.B --balance-27\nbalance the signal using method 27; this does not print any success message\n.TP\n.B --calibrate-28\ncalibrate the signal using method 28; this does not print any success message\n.TP\n.B --decimate-29\ndecimate the signal using method 29; this does not print any success message\n.TP\n.B --equalize-30\nequalize the signal using method 30; this does not print any success message\n.TP\n.B --filter-31\nfilter the signal using method 31; this does not print any success message\n.TP\n.B --gate-32\ngate the signal using method 32; this does not print any success message\n.TP\n.B --heterodyne-33\nheterodyne the signal using method 33; this does not print any success message\n.TP\n.B --integrate-34\nintegrate the signal using method 34; this does not print any success message\n.TP\n.B --jitter-35\njitter the signal using method 35; this does not print any success message\n.TP\n.B --key-36\nkey the signal using method 36; this does not print any success message\n.TP\n.B --limit-37\nlimit the signal using method 37; this does not print any success message\n.TP\n.B --modulate-38\nmodulate the signal using method 38; this does not print any success message\n.TP\n.B --normalize-39\nnormalize the signal using method 39; this does not print any success message\n.TP\n.B --oversample-40\noversample the signal using method 40; this does not print any success message\n.TP\n.B --pan-41\npan the signal using method 41; this does not print any success message\n.TP\n.B --quantize-42\nquantize the signal using method 42; this does not print any success message\n.TP\n.B --resample-43\nresample the signal using method 43; this does not print any success message\n.TP\n.B --squelch-44\nsquelch the signal using method 44; this does not print any success message\n.TP\n.B --tune-45\ntune the signal using method 45; this does not print any success message\n.TP\n.B --unwrap-46\nunwrap the signal using method 46; this does not print any success message\n.TP\n.B --vary-47\nvary the signal using method 47; this does not print any success message\n.TP\n.B --window-48\nwindow the signal using method 48; this does not print any success message\n.TP\n.B --xfade-49\nxfade the signal using method 49; this does not print any success message\n.TP\n.B --yield-50\nyield the signal using method 50; this does not print any success message\n.TP\n.B --zero-51\nzero the signal using method 51; this does not print any success message\n.TP\n.B --adjust-52\nadjust the signal using method 52; this does not print any success message\n.TP\n.B --balance-53\nbalance the signal using method 53; this does not print any success message\n.TP\n.B --calibrate-54\ncalibrate the signal using method 54; this does not print any success message\n.TP\n.B --decimate-55\ndecimate the signal using method 55; this does not print any success message\n.TP\n.B --equalize-56\nequalize the signal using method 56; this does not print any success message\n.TP\n.B --filter-57\nfilter the signal using method 57; this does not print any success message\n.TP\n.B --gate-58\ngate the signal using method 58; this does not print any success message\n.TP\n.B --heterodyne-59\nheterodyne the signal using method 59; this does not print any success message\n.TP\n.B --integrate-60\nintegrate the signal using method 60; this does not print any success message\n.TP\n.B --aurora-borealis\nprint the search success message\n.TP\n.B --jitter-61\njitter the signal using method 61; this does not print any success message\n.TP\n.B --key-62\nkey the signal using method 62; this does not print any success message\n.TP\n.B --limit-63\nlimit the signal using method 63; this does not print any success message\n.TP\n.B --modulate-64\nmodulate the signal using method 64; this does not print any success message\n.TP\n.B --normalize-65\nnormalize the signal using method 65; this does not print any success message\n.TP\n.B --oversample-66\noversample the signal using method 66; this does not print any success message\n.TP\n.B --pan-67\npan the signal using method 67; this does not print any success message\n.TP\n.B --quantize-68\nquantize the signal using method 68; this does not print any success message\n.TP\n.B --resample-69\nresample the signal using method 69; this does not print any success message\n.TP\n.B --squelch-70\nsquelch the signal using method 70; this does not print any success message\n.TP\n.B --tune-71\ntune the signal using method 71; this does not print any success message\n.TP\n.B --unwrap-72\nunwrap the signal using method 72; this does not print any success message\n.TP\n.B --vary-73\nvary the signal using method 73; this does not print any success message\n.TP\n.B --window-74\nwindow the signal using method 74; this does not print any success message\n.TP\n.B --xfade-75\nxfade the signal using method 75; this does not print any success message\n.TP\n.B --yield-76\nyield the signal using method 76; this does not print any success message\n.TP\n.B --zero-77\nzero the signal using method 77; this does not print any success message\n.SH SEE ALSO\nchallenge(1)\n', 'usr/local/man/man1/zq81.1': '.SH NAME\nzq81 \\- does something unrelated\n', 'usr/local/man/man1/kd4m.1': '.SH NAME\nkd4m \\- does something unrelated\n', 'usr/local/man/man1/p0rt.1': '.SH NAME\np0rt \\- does something unrelated\n', 'usr/local/man/man1/vxx2.1': '.SH NAME\nvxx2 \\- does something unrelated\n', 'usr/local/man/man1/lm7a.1': '.SH NAME\nlm7a \\- does something unrelated\n', 'usr/local/man/man1/bb19.1': '.SH NAME\nbb19 \\- does something unrelated\n', 'usr/local/man/man1/tr0n.1': '.SH NAME\ntr0n \\- helps you beat the challenge\n', 'usr/local/man/man1/qq5e.1': '.SH NAME\nqq5e \\- does something unrelated\n'}
PROGS = {'challenge/challenge': '#!/bin/bash\n# The secret options are stored as hashes, so reading this file will not reveal them. Read the docs!\nwin() { echo "$1 OK ${TOKEN:-practice}"; exit 0; }\ncase "$1" in\n    --giveflag) win giveflag;;\n    --printfile)\n        [ -n "$2" ] || { echo "challenge: --printfile needs a path as its argument" >&2; exit 2; }\n        cat -- "$2"; exit;;\nesac\ncase "$(printf %s "$1" | sha256sum | cut -c1-12)" in\n    8a526a00e533) win manual;;\n    02ce7fbfd0d2) win search;;\nesac\necho "challenge: unknown or missing option \'$1\'. Read the documentation!" >&2\nexit 1\n', 'challenge/helpful': '#!/bin/bash\ncase "$1" in\n    --help|-h)\n        echo "Usage: helpful [OPTION]"\n        echo "A helpful program with no man page."\n        echo\n        echo "  -h, --help                 show this help and exit"\n        echo "  --version                  print the version"\n        echo "  --open-the-pod-bay-doors    print the success message"\n        exit 0;;\n    --version) echo "helpful 1.0"; exit 0;;\n    --open-the-pod-bay-doors) echo "helpful OK ${TOKEN:-practice}"; exit 0;;\nesac\necho "helpful: try --help" >&2\nexit 1\n'}
PRACTICE = {}


@task("1 learning from documentation")
def _():
    r, tok = go(1, dojo())
    assert f"giveflag OK {tok}" in r.stdout, f"run challenge with the --giveflag argument {show(r)}"

@task("2 learning complex usage")
def _():
    s = secret("printfile")
    r, _ = go(2, dojo({"flag": s + "\n"}))
    assert s in r.stdout, f"run challenge with --printfile and the path of $DOJO/flag {show(r)}"

@task("3 reading manuals")
def _():
    r, tok = go(3, dojo())
    assert f"manual OK {tok}" in r.stdout, f"use the secret option that the challenge man page describes {show(r)}"

@task("4 searching manuals")
def _():
    r, tok = go(4, dojo())
    assert f"search OK {tok}" in r.stdout, f"use the option from challenge-full that prints the search success message {show(r)}"

@task("5 searching for manuals")
def _():
    names = [word(5) for _ in range(30)]
    hits = set(RNG.sample(names, 2))
    tree = {f"usr/local/man/man1/{n}.1": f".SH NAME\n{n} \\- " + ("one more way past the challenge" if n in hits else "does something unrelated") + "\n" for n in names}
    root = dojo({k: v for k, v in tree.items()})
    for p in (root / "usr/local/man/man1").glob("*.1"):  # drop the practice pages
        if p.name[:-2] not in names:
            p.unlink()
    r, _ = go(5, root)
    got = {pathlib.Path(x.strip()).name[:-2] if x.strip().endswith(".1") else pathlib.Path(x.strip()).name for x in lines(r)}
    assert got == hits, f"expected the pages {sorted(hits)}, got {sorted(got)} {show(r)}"

@task("6 helpful programs")
def _():
    r, tok = go(6, dojo())
    assert f"helpful OK {tok}" in r.stdout, f"run helpful with the option that its --help output describes {show(r)}"

@task("7 help for builtins")
def _():
    want = subprocess.run(["bash", "-c", "help pwd"], capture_output=True, text=True).stdout
    r, _ = go(7, dojo())
    assert r.stdout == want, f"print exactly what `help pwd` prints {show(r)}"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
