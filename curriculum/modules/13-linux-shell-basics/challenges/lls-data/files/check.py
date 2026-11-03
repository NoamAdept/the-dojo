#!/usr/bin/env python3
"""Run with ./check. Tests each task in answers/task1.sh to answers/task6.sh and lists what still fails."""
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
RNG = random.Random(108)


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

TREE = {'challenge/flags.txt': 'academy{s8n628vdgrjq}\nacademy{womqel1hak6d}\nacademy{hi74uu5m4q91}\nacademy{irq722olhwf2}\nacademy{j0462cqig92l}\nacademy{kn8ootxo6whr}\nacademy{fjrgxjl0qk1o}\nacademy{83ltmmhv131n}\nacademy{gtjkbnbkngjo}\nacademy{618jwehfkbr6}\nacademy{6klesa5ldshe}\nacademy{72xckbhl5m8q}\nacademy{ixhtmqiqq2q9}\nacademy{c0uwre2txile}\nacademy{4i7f22wcr30u}\nacademy{7awjf1xq37l8}\nacademy{gu3mec77afh8}\nacademy{0vp3hfhxxr3u}\nacademy{k0382734u25w}\nacademy{wvkak4moojng}\nacademy{clr780o5b2nt}\nacademy{o2r3nvkqqt1f}\nacademy{dh4rer81kng7}\nacademy{t7xo6k60u9fo}\nacademy{2x56ob1l717u}\nacademy{ij52wxf663kb}\nacademy{4fbftpgnpmq5}\nacademy{owfqaqxu9p9a}\nacademy{6vuxsb8hc9wk}\nacademy{eiqhdj1huocb}\nacademy{nfku9qudt1u4}\nacademy{p2tef4dgfcg8}\nacademy{b2ga2kbr5575}\nacademy{gi2msl01llro}\nacademy{v4dvp8k7h4r7}\nacademy{sxg6xnnsig6l}\nacademy{x7vwm3ib9bnt}\nacademy{769lqjbtujb4}\nacademy{6bpm6hho382u}\nacademy{whfwmlps4mv7}\nacademy{9h677bcqp89p}\nacademy{cxabcgni1sqo}\nacademy{kjvxju1c06ev}\nacademy{bxtccxd2ws7i}\nacademy{98t531new4v1}\nacademy{lklm8525ld4c}\nacademy{revk62q4capv}\nacademy{u4rdvj1ttpsb}\nacademy{t2gnnsxnpe0d}\nacademy{gn9tcad1apwa}\nacademy{zz_practice_sort}\nacademy{187asvb31psk}\nacademy{q23fp2pv1ef6}\nacademy{oucal7m73iht}\nacademy{jvfh1lmk53r5}\nacademy{06151aw2u3cw}\nacademy{lculum2ojp5i}\nacademy{bq7wolpbombn}\nacademy{qsesumhawov2}\nacademy{9a1t56kf33st}\nacademy{ln04cp6lj7s5}\nacademy{df39907eidew}\nacademy{qwkctb52716c}\nacademy{g56tpe6vmps7}\nacademy{isod70tj4lmc}\nacademy{v4nr4xdfm3lf}\nacademy{rs5gdkaddtqn}\nacademy{cququ2i1b619}\nacademy{iwx3u2cdhvr2}\nacademy{mtci96sjqs4d}\nacademy{9vionarjtuxe}\nacademy{nii1tnmjfx00}\nacademy{8x91a30dtmn2}\nacademy{vbf0hrl36sjg}\nacademy{fvqgl21r2af8}\nacademy{qwl8h1a21v3t}\nacademy{txwqnxaib486}\nacademy{qmsthgsix9k8}\nacademy{x2qveth1k7v8}\nacademy{hh6r4n2wvscj}\nacademy{mbopk3hd2kkp}\nacademy{i28qgq5vec5x}\nacademy{770i4rhuthi3}\nacademy{bfva99btp09p}\nacademy{3bbjc893x9do}\nacademy{6rob1h6879i8}\nacademy{om4c0n9uf4mv}\nacademy{6ku1mxsqtjs9}\nacademy{tocibjakhc83}\nacademy{3qb70a7pnxh5}\nacademy{tsk9dktwnkmm}\nacademy{lijhb7welfir}\nacademy{hs8ulbxxs34q}\nacademy{ri3food4nwd3}\nacademy{v7ron0jnwnps}\nacademy{n6v9ke0n4085}\nacademy{dkric11ksnds}\nacademy{l7woeu8jic7b}\nacademy{5r1mo0vbuh8o}\nacademy{dwrjri654sk4}\nacademy{0kur6lqekcp5}\n'}
PROGS = {'challenge/swapcase': '#!/bin/bash\necho "@SWAP@"\n', 'challenge/carets': '#!/bin/bash\necho "@CARETS@"\n', 'challenge/newlines': '#!/bin/bash\nprintf "@NEWLINES@\\n"\n', 'challenge/pwn': '#!/bin/bash\nprintf "@ALL@\\n"\n', 'challenge/college': '#!/bin/bash\n[ "$(sha256sum | cut -c1-16)" = "@HASH@" ] || { echo "college: I wanted exactly the first 7 lines of pwn\'s output" >&2; exit 1; }\necho "college OK ${TOKEN:-practice}"\n', 'challenge/columns': '#!/bin/bash\nprintf "@COLS@"\n'}
PRACTICE = {'@SWAP@': 'ACADEMY{PRACTICE_TR}', '@CARETS@': 'a^c%a^demy{pr%actice_d^el}', '@NEWLINES@': 'acad\\nemy{pra\\nctice\\n_nl}', '@ALL@': 'practice line 0 249523\\npractice line 1 621429\\npractice line 2 570665\\npractice line 3 136758\\npractice line 4 387926\\npractice line 5 960437\\npractice line 6 633256\\nextra line 0 497081\\nextra line 1 656115\\nextra line 2 609067\\nextra line 3 68711\\nextra line 4 635017\\nextra line 5 13807\\nextra line 6 952965\\nextra line 7 878149\\nextra line 8 492025\\nextra line 9 271952\\nextra line 10 577539\\nextra line 11 245713\\nextra line 12 201058\\nextra line 13 1044009\\nextra line 14 751984\\nextra line 15 493107\\nextra line 16 567252\\nextra line 17 877093\\nextra line 18 576330\\nextra line 19 499492\\nextra line 20 416425\\nextra line 21 670111\\nextra line 22 902847\\nextra line 23 157932\\nextra line 24 243187\\nextra line 25 665699\\nextra line 26 158987\\nextra line 27 910211\\nextra line 28 970808\\nextra line 29 548595\\nextra line 30 408878\\nextra line 31 777258\\nextra line 32 15882\\nextra line 33 704025\\nextra line 34 814989\\nextra line 35 67141\\nextra line 36 167142\\nextra line 37 795062\\nextra line 38 1004008\\nextra line 39 619812', '@HASH@': '88a094f917253302', '@COLS@': '2402 a\\n10871 c\\n26561 a\\n2016 d\\n27986 e\\n29361 m\\n9828 y\\n16491 {\\n20488 p\\n24554 r\\n31151 a\\n29796 c\\n13701 t\\n24400 i\\n26824 c\\n31182 e\\n14989 _\\n13942 c\\n24859 u\\n27244 t\\n19904 }\\n'}


import hashlib

def esc(s):
    return s.replace("\n", "\\n")

@task("1 translating characters")
def _():
    s = secret("tr")
    r, _ = go(1, dojo(subs={"@SWAP@": s.swapcase()}))
    assert r.stdout.strip() == s, f"swap the case back with tr {show(r)}"

@task("2 deleting characters")
def _():
    s = secret("del")
    noisy = "".join(c + RNG.choice(["", "", "^", "%", "^%"]) for c in s)
    r, _ = go(2, dojo(subs={"@CARETS@": noisy}))
    assert r.stdout.strip() == s, f"delete every ^ and % with tr -d {show(r)}"

@task("3 deleting newlines")
def _():
    s = secret("nl")
    noisy = "".join(c + RNG.choice(["", "\n"]) for c in s)
    r, _ = go(3, dojo(subs={"@NEWLINES@": esc(noisy)}))
    assert r.stdout.rstrip("\n") == s and "\n" not in r.stdout.rstrip("\n"), f"delete every newline with tr -d {show(r)}"

@task("4 extracting the first lines with head")
def _():
    first = [f"{word()} line {i}" for i in range(7)]
    allines = first + [f"{word()} extra {i}" for i in range(RNG.randint(20, 60))]
    h = hashlib.sha256(("\n".join(first) + "\n").encode()).hexdigest()[:16]
    r, tok = go(4, dojo(subs={"@ALL@": esc("\n".join(allines)), "@HASH@": h}))
    assert f"college OK {tok}" in r.stdout, f"pipe pwn through head (first 7 lines) into college {show(r)}"

@task("5 extracting columns with cut")
def _():
    s = secret("cut")
    cols = "".join(f"{RNG.randint(1000, 32767)} {c}\n" for c in s)
    r, _ = go(5, dojo(subs={"@COLS@": esc(cols)}))
    assert r.stdout.rstrip("\n") == s, f"cut out the 2nd column and join the characters into 1 line {show(r)}"

@task("6 sorting data")
def _():
    fakes = ["academy{%s}" % "".join(RNG.choice("0123456789abcdefghijklmnopqrstuvwx") for _ in range(12)) for _ in range(100)]
    real = "academy{zz" + word(10) + "}"
    fakes.insert(RNG.randrange(100), real)
    r, _ = go(6, dojo({"challenge/flags.txt": "\n".join(fakes) + "\n"}))
    assert r.stdout.strip() == real, f"sort the file and print only its last line {show(r)}"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
