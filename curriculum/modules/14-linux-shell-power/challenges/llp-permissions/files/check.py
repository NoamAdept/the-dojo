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

import grp, random, stat

RNG = random.Random(777)

def mode(p):
    return stat.S_IMODE(os.stat(p).st_mode)

def make(d, rel, m, text="data\n"):
    p = d / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    p.chmod(m)
    return p

@task("1 read the modes")
def _():
    answer(1)
    d = sandbox()
    names = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf"]
    choices = [0o644, 0o640, 0o600, 0o604, 0o755, 0o750, 0o700, 0o666, 0o660]
    want = []
    for n in names:
        m = RNG.choice(choices)
        make(d, f"box/{n}.txt", m)
        if m & 0o004:
            want.append(f"{n}.txt")
    r, _ = run(1, cwd=d)
    got = r.stdout.split()
    assert got == sorted(want), f"printed {got}, expected {sorted(want)}"

@task("2 symbolic chmod")
def _():
    answer(2)
    for start in (0o604, RNG.choice([0o755, 0o744, 0o407, 0o645])):
        d = sandbox()
        p = make(d, "notes.txt", start)
        run(2, cwd=d)
        want = (start | 0o020) & ~0o007
        assert mode(p) == want, f"started at {start:o}, got {mode(p):o}, expected {want:o}"

@task("3 octal chmod")
def _():
    answer(3)
    d = sandbox()
    s = make(d, "secret.txt", 0o666)
    x = make(d, "run.sh", 0o644, "#!/bin/bash\necho run\n")
    run(3, cwd=d)
    assert mode(s) == 0o600, f"secret.txt is {mode(s):o}, expected 600"
    assert mode(x) == 0o750, f"run.sh is {mode(x):o}, expected 750"

@task("4 execute bit")
def _():
    answer(4)
    token = "ping-%06d" % RNG.randint(0, 999999)
    d = sandbox()
    p = make(d, "hello.sh", 0o644, f"#!/bin/bash\necho \"hello says {token}\"\n")
    r, _ = run(4, cwd=d)
    assert mode(p) & 0o100, "hello.sh is not executable by its owner"
    assert token in r.stdout, "run ./hello.sh in your script. Do not hide its output"

@task("5 umask")
def _():
    a = answer(5)
    assert "umask" in a.read_text(), "use the umask command"
    # chmod does nothing during this run, so only umask can give the right modes.
    stub = sandbox({"chmod": "#!/bin/sh\nexit 0\n"})
    (stub / "chmod").chmod(0o755)
    r, d = run(5, env={"PATH": f"{stub}{os.pathsep}{os.environ.get('PATH', '')}"})
    f, g = d / "private.log", d / "logs"
    assert f.is_file() and g.is_dir(), "create the file private.log and the directory logs"
    assert mode(f) == 0o640, f"private.log is {mode(f):o}, expected 640"
    assert mode(g) == 0o750, f"logs is {mode(g):o}, expected 750"

@task("6 find setuid files")
def _():
    answer(6)
    d = sandbox()
    want = []
    for n in ["scan", "tune", "record", "replay", "decode", "upload"]:
        m = RNG.choice([0o755, 0o4755, 0o2755, 0o750, 0o4750, 0o1755])
        make(d, f"bin/{n}", m, "#!/bin/sh\n")
        if m & 0o4000:
            want.append(n)
    r, _ = run(6, cwd=d)
    assert r.stdout.split() == sorted(want), f"printed {r.stdout.split()}, expected {sorted(want)}"

@task("7 chgrp")
def _():
    answer(7)
    mine = sorted(set(os.getgroups()) - {os.getegid()}) or [os.getegid()]
    gid = mine[-1]
    try:
        name = grp.getgrgid(gid).gr_name
    except KeyError:
        name = str(gid)
    d = sandbox({"group.txt": name + "\n"})
    p = make(d, "shared.txt", 0o664)
    run(7, cwd=d)
    assert os.stat(p).st_gid == gid, f"shared.txt's group is gid {os.stat(p).st_gid}, expected {name} ({gid})"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
