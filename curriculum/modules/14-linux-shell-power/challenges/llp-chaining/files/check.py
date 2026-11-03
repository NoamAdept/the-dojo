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

import random, re

RNG = random.Random(99)

def helper(name, code):
    return f"#!/bin/bash\necho {name} >> log.txt\nexit {code}\n"

def box(**codes):
    d = sandbox({n: helper(n, c) for n, c in codes.items()})
    for n in codes:
        (d / n).chmod(0o755)
    return d

def log(d):
    p = d / "log.txt"
    return p.read_text().split() if p.exists() else []

def chain(n, a, b, cases):
    answer(n)
    for code, want in cases:
        d = box(**{a: code, b: 0})
        run(n, cwd=d)
        ok = "succeeds" if code == 0 else "fails"
        assert log(d) == want, f"when ./{a} {ok}, ran {log(d)}, expected {want}"

@task("1 semicolon")
def _():
    chain(1, "first", "second", [(0, ["first", "second"]), (1, ["first", "second"])])

@task("2 success only (&&)")
def _():
    chain(2, "build", "deploy", [(0, ["build", "deploy"]), (1, ["build"])])

@task("3 fallback (||)")
def _():
    chain(3, "primary", "backup", [(0, ["primary"]), (1, ["primary", "backup"])])

@task("4 arguments")
def _():
    answer(4)
    words = ["antenna", "mixer", "filter", "tuner", "decoder", "sample"]
    for k in (2, 4):
        args = RNG.sample(words, k)
        r, _ = run(4, args=args)
        want = [f"{args[1]} {args[0]}", str(k)]
        assert r.stdout.strip().splitlines() == want, f"args {args}: printed {r.stdout.strip().splitlines()}, expected {want}"

@task("5 if / else")
def _():
    answer(5)
    d = sandbox({"present.cfg": "x\n"})
    (d / "adir").mkdir()
    for name, out, code in [("present.cfg", "found present.cfg", 0), ("absent.cfg", "missing absent.cfg", 1),
                            ("adir", "missing adir", 1)]:
        r, _ = run(5, cwd=d, args=[name])
        assert r.stdout.strip() == out, f"for {name!r} printed {r.stdout.strip()!r}, expected {out!r}"
        assert r.returncode == code, f"for {name!r} exit code {r.returncode}, expected {code}"

@task("6 elif")
def _():
    answer(6)
    cases = {-RNG.randint(1, 50): "negative", 0: "zero", 1: "small", 9: "small", 10: "large", RNG.randint(11, 999): "large"}
    for v, want in cases.items():
        r, _ = run(6, args=[str(v)])
        assert r.stdout.strip() == want, f"for {v} printed {r.stdout.strip()!r}, expected {want!r}"

@task("7 shebang")
def _():
    answer(7)
    r, d = run(7)
    h = d / "hello"
    assert h.is_file(), "your script should create ./hello"
    assert re.match(r"#!\s*(/usr)?/bin/(env\s+)?bash\b", h.read_text()), "./hello must start with #!/bin/bash"
    assert os.access(h, os.X_OK) and h.stat().st_mode & 0o100, "./hello is not executable (chmod +x)"
    name = RNG.choice(["Ada", "Grace", "Linus"])
    out = subprocess.run([str(h), name], cwd=d, capture_output=True, text=True, timeout=10).stdout.strip()
    assert out == f"Hello, {name}!", f"./hello {name} printed {out!r}"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
