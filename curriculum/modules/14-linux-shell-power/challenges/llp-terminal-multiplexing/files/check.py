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

import random, time

RNG = random.Random(31337)
os.environ.pop("TMUX", None)  # do not talk to a tmux the learner may be sitting in

def need_tmux():
    if not shutil.which("tmux"):
        extra = " (screen is installed, but these tasks use tmux)" if shutil.which("screen") else ""
        raise AssertionError("tmux is not installed" + extra + ". Install it with: sudo apt install tmux")

def env(d):
    return {"TMUX_TMPDIR": str(d), "SHELL": "/bin/sh"}

def tm(d, *a):
    return subprocess.run(["tmux", *a], env={**os.environ, "HOME": str(d), **env(d)},
                          capture_output=True, text=True, timeout=10)

def sessions(d):
    r = tm(d, "ls", "-F", "#S")
    return r.stdout.split() if r.returncode == 0 else []

def word(prefix):
    return prefix + "-" + "".join(RNG.choice("abcdefghjkmnpqrstuvwxyz") for _ in range(5))

def setup(n, extra=None):
    """Sandbox with name.txt holding a fresh session name."""
    need_tmux()
    answer(n)
    name = word("radio")
    return sandbox({"name.txt": name + "\n", **(extra or {})}), name

def go(n, d):
    r, _ = run(n, cwd=d, env=env(d))
    return r

@task("1 start a detached session")
def _():
    d, name = setup(1)
    try:
        go(1, d)
        assert sessions(d) == [name], f"sessions running: {sessions(d)}, expected [{name!r}]"
    finally:
        tm(d, "kill-server")

@task("2 list sessions")
def _():
    need_tmux()
    answer(2)
    names = [word("sdr") for _ in range(3)]
    d = sandbox()
    try:
        for s in names:
            tm(d, "new-session", "-d", "-s", s)
        r = go(2, d)
        assert sorted(r.stdout.split()) == sorted(names), f"printed {r.stdout.split()}, expected {sorted(names)}"
    finally:
        tm(d, "kill-server")

@task("3 send keys")
def _():
    token = word("token")
    d, name = setup(3, {"token.txt": token + "\n"})
    tm(d, "new-session", "-d", "-s", name, "-c", str(d))
    try:
        go(3, d)
        out = d / "out.txt"
        for _ in range(100):
            if out.exists() and out.read_text().strip():
                break
            time.sleep(0.05)
        assert out.exists(), "out.txt never appeared. Did you press Enter (send-keys ... Enter)?"
        assert out.read_text().strip() == token, f"out.txt has {out.read_text().strip()!r}, expected the token"
    finally:
        tm(d, "kill-server")

@task("4 new window")
def _():
    d, name = setup(4)
    tm(d, "new-session", "-d", "-s", name, "-c", str(d))
    try:
        go(4, d)
        wins = tm(d, "list-windows", "-t", name, "-F", "#W").stdout.split()
        assert "logs" in wins, f"windows in {name}: {wins}, expected one named logs"
        assert len(wins) >= 2, f"windows in {name}: {wins}. Add a new window (new-window -n logs), do not rename the one that is there"
    finally:
        tm(d, "kill-server")

@task("5 read the screen")
def _():
    secret = word("secret")
    d, name = setup(5)
    tm(d, "new-session", "-d", "-s", name, "-c", str(d), f"echo {secret}; sleep 600")
    try:
        for _ in range(100):
            if secret in tm(d, "capture-pane", "-p", "-t", name).stdout:
                break
            time.sleep(0.05)
        r = go(5, d)
        assert secret in r.stdout, "your output does not have the text that the pane shows (use capture-pane -p)"
    finally:
        tm(d, "kill-server")

@task("6 kill one session")
def _():
    d, name = setup(6)
    others = [word("keep") for _ in range(2)]
    for s in [others[0], name, others[1]]:
        tm(d, "new-session", "-d", "-s", s)
    try:
        go(6, d)
        left = sessions(d)
        assert name not in left, f"{name} is still running"
        assert sorted(left) == sorted(others), f"sessions left: {left}, expected {sorted(others)}"
    finally:
        tm(d, "kill-server")

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
