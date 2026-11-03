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

import random

RNG = random.Random(2718)
SYS = os.environ["PATH"]

def tag():
    return "".join(RNG.choice("abcdefghjkmnpqrstuvwxyz") for _ in range(5))

def prog(d, rel, text, exe=True):
    p = d / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    p.chmod(0o755 if exe else 0o644)
    return p

@task("1 read PATH")
def _():
    answer(1)
    path = ":".join(f"/opt/academy-{tag()}" for _ in range(3)) + ":" + SYS
    r, _ = run(1, env={"PATH": path})
    assert r.stdout.strip().splitlines() == path.split(":"), f"printed {r.stdout.strip().splitlines()}, expected {path.split(':')}"

@task("2 find a command")
def _():
    answer(2)
    d = sandbox()
    name = "zapper-" + tag()
    prog(d, f"d1/{name}", "#!/bin/sh\n", exe=False)  # not executable: skipped by the lookup
    want = prog(d, f"d2/{name}", "#!/bin/sh\necho zap\n")
    prog(d, f"d3/{name}", "#!/bin/sh\necho zap\n")
    r, _ = run(2, cwd=d, args=[name], env={"PATH": f"{d}/d1:{d}/d2:{d}/d3:{SYS}"})
    assert r.stdout.strip() == str(want), f"printed {r.stdout.strip()!r}, expected {str(want)!r}"

@task("3 use PATH")
def _():
    answer(3)
    token = "beacon-" + tag()
    d = sandbox()
    prog(d, "tools/beacon", "#!/bin/bash\nif command -v beacon >/dev/null; then echo " + token +
         "; else echo 'beacon: tools/ is not on PATH'; fi\n")
    r, _ = run(3, cwd=d)
    assert token in r.stdout, f"beacon said {r.stdout.strip()!r}. Add tools/ to PATH with export, then run beacon"

@task("4 your own bin")
def _():
    answer(4)
    r, d = run(4)
    h = d / "bin" / "hello-pi"
    assert h.is_file() and h.stat().st_mode & 0o100, "create an executable $HOME/bin/hello-pi"
    assert "hello from pi" in r.stdout, "run hello-pi at the end of your script"
    assert (d / ".bashrc").exists(), "add the PATH line to $HOME/.bashrc"
    e = {**os.environ, "HOME": str(d), "PATH": SYS}
    out = subprocess.run(["bash", "-c", "source ~/.bashrc >/dev/null 2>&1; hello-pi"], cwd=d, env=e,
                         capture_output=True, text=True, timeout=10).stdout
    assert "hello from pi" in out, "a new shell that reads ~/.bashrc cannot run hello-pi"

@task("5 shadow a command")
def _():
    answer(5)
    report = "#!/bin/bash\necho \"Report year: $(date +%Y)\"\n"
    d = sandbox()
    prog(d, "report.sh", report)
    r, _ = run(5, cwd=d)
    assert (d / "report.sh").read_text() == report, "do not edit report.sh"
    assert "Report year: 1999" in r.stdout, f"report.sh printed {r.stdout.strip()!r}"

@task("6 every match")
def _():
    answer(6)
    for order in (["a", "b", "c"], ["c", "a", "b"]):
        d = sandbox()
        for x in "abc":
            prog(d, f"{x}/tool", "#!/bin/sh\n")
        path = ":".join(f"{d}/{x}" for x in order) + ":" + SYS
        r, _ = run(6, cwd=d, env={"PATH": path})
        want = [f"{d}/{x}/tool" for x in order]
        assert r.stdout.strip().splitlines() == want, f"with PATH order {order} printed {r.stdout.strip().splitlines()}, expected {want}"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
