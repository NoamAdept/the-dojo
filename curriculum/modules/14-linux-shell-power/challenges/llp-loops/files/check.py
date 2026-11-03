#!/usr/bin/env python3
"""Run with ./check. Tests each task in answers/ and lists what still fails."""
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

import hashlib, random

RNG = random.Random(5150)
WORDS = ["alpha", "bravo", "carrier", "delta", "echo", "fm", "gain", "hilbert", "iq", "jitter"]

def lines(r):
    return r.stdout.strip().splitlines()

def blob(n):
    return bytes(RNG.randrange(256) for _ in range(n))

def folder(spec):
    """spec: {name: size}. Returns (sandbox, {name: bytes}) with files under in/."""
    data = {n: blob(s) for n, s in spec.items()}
    d = sandbox({"in/" + n: b for n, b in data.items()})
    (d / "in").mkdir(exist_ok=True)
    return d, data

def names(k, ext, spaces=False):
    pick = RNG.sample(WORDS, k)
    if spaces:
        pick = [w + " " + RNG.choice(WORDS) for w in pick[:-1]] + [pick[-1] + "  two"]
    return [p + ext for p in pick]

@task("1 first loop")
def _():
    answer(1)
    txt = names(4, ".txt")
    d, _ = folder({**{n: 5 for n in txt}, "readme.md": 3, "data.log": 3})
    for arg in ("in", str(d / "in")):
        r, _ = run(1, cwd=d, args=[arg])
        assert sorted(lines(r)) == sorted(txt), f"with folder {arg!r} printed {lines(r)}, expected {sorted(txt)} (names only, no folder part, only .txt files)"

@task("2 empty folders (nullglob)")
def _():
    answer(2)
    k = RNG.randint(2, 5)
    d, _ = folder({**{n: 1 for n in names(k, ".log")}, "keep.txt": 1})
    r, _ = run(2, cwd=d, args=["in"])
    assert lines(r)[-1:] == [str(k)], f"folder with {k} .log files: printed {lines(r)}, expected {k}"
    d, _ = folder({"only.txt": 1})
    r, _ = run(2, cwd=d, args=["in"])
    assert lines(r)[-1:] == ["0"], f"folder with no .log files: printed {lines(r)}, expected 0. Did you add shopt -s nullglob?"

@task("3 spaces survive")
def _():
    answer(3)
    txt = names(3, ".txt", spaces=True)
    d, data = folder({**{n: 20 for n in txt}, "skip me.log": 4})
    (d / "out").mkdir()
    run(3, cwd=d, args=["in", "out"])
    got = sorted(p.name for p in (d / "out").iterdir())
    want = sorted(n + ".bak" for n in txt)
    assert got == want, f"out/ holds {got}, expected {want}. Quote every variable: \"$f\""
    for n in txt:
        assert (d / "out" / (n + ".bak")).read_bytes() == data[n], f"out/{n}.bak is not an exact copy of in/{n}"

@task("4 size of one file")
def _():
    answer(4)
    for size in (RNG.randint(1, 99), RNG.randint(1000, 5000)):
        name = RNG.choice(WORDS) + " capture.iq"
        d = sandbox({name: blob(size)})
        r, _ = run(4, cwd=d, args=[name])
        assert lines(r) == [str(size)], f"for a {size}-byte file printed {lines(r)}, expected only {size}"

@task("5 total size")
def _():
    answer(5)
    sizes = {n: RNG.randint(10, 900) for n in names(4, ".dat", spaces=True)}
    d, _ = folder({**sizes, "ignore.txt": 77})
    r, _ = run(5, cwd=d, args=["in"])
    want = str(sum(sizes.values()))
    assert lines(r)[-1:] == [want], f"printed {lines(r)}, expected {want} (the .dat files only)"
    d, _ = folder({"ignore.txt": 77})
    r, _ = run(5, cwd=d, args=["in"])
    assert lines(r)[-1:] == ["0"], f"with no .dat files printed {lines(r)}, expected 0"

@task("6 fingerprint")
def _():
    answer(6)
    data = blob(RNG.randint(50, 500))
    name = "my " + RNG.choice(WORDS) + ".bin"
    d = sandbox({name: data})
    r, _ = run(6, cwd=d, args=[name])
    want = hashlib.sha256(data).hexdigest()
    assert lines(r) == [want], f"printed {lines(r)}, expected just the 64-character hash {want}"

@task("7 sorted report")
def _():
    answer(7)
    txt = names(4, ".txt", spaces=True)
    sizes = dict(zip(txt, RNG.sample(range(5, 3000), len(txt))))
    d, _ = folder({**sizes, "big.log": 9999})
    r, _ = run(7, cwd=d, args=["in"])
    want = [f"{s} {n}" for n, s in sorted(sizes.items(), key=lambda x: x[1])]
    assert lines(r) == want, f"printed {lines(r)}, expected {want}"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
