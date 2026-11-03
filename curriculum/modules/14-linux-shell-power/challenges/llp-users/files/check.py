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

def make_passwd(seed):
    """Return /etc/passwd-style text with a few system and human accounts."""
    import random
    rng = random.Random(seed)
    rows = [("root", 0, 0, "root", "/root", "/bin/bash"),
            ("daemon", 1, 1, "daemon", "/usr/sbin", "/usr/sbin/nologin"),
            ("sync", 4, 65534, "sync", "/bin", "/bin/sync"),
            ("nobody", 65534, 65534, "nobody", "/nonexistent", "/usr/sbin/nologin")]
    names = ["ada", "grace", "linus", "ken", "dennis", "radia", "barbara", "alan", "margaret", "edsger"]
    rng.shuffle(names)
    uid = 1000
    for n in names[:rng.randint(3, 5)]:
        rows.append((n, uid, uid, n.title(), "/home/" + n, rng.choice(["/bin/bash", "/bin/bash", "/bin/zsh", "/bin/sh"])))
        uid += rng.randint(1, 3)
    for n, u in [("postgres", 100 + rng.randint(0, 20)), ("sdrd", 120 + rng.randint(0, 20))]:
        rows.append((n, u, u, n + " service", "/var/lib/" + n, rng.choice(["/bin/bash", "/usr/sbin/nologin"])))
    rows.append((rng.choice(["toor", "backup2", "sysadm"]), 0, 0, "", "/root", "/bin/bash"))
    rng.shuffle(rows)
    rows.sort(key=lambda r: r[0] != "root")  # root stays first, like a real file
    return "".join(f"{n}:x:{u}:{g}:{c}:{h}:{s}\n" for n, u, g, c, h, s in rows)

import grp, pwd

def rows(text):
    return [l.split(":") for l in text.splitlines() if l]

def lines(r):
    return r.stdout.strip().splitlines()

@task("1 whoami")
def _():
    r, _ = run(1)
    me = pwd.getpwuid(os.getuid()).pw_name
    assert r.stdout.strip() == me, f"printed {r.stdout.strip()!r}, expected {me!r}"

@task("2 uid and gid")
def _():
    r, _ = run(2)
    want = f"{os.getuid()} {os.getgid()}"
    assert r.stdout.strip() == want, f"printed {r.stdout.strip()!r}, expected {want!r}"

@task("3 groups")
def _():
    r, _ = run(3)
    want = set()
    for g in set(os.getgroups()) | {os.getegid()}:
        try:
            want.add(grp.getgrgid(g).gr_name)
        except KeyError:
            want.add(str(g))
    got = set(lines(r))
    assert got == want, f"printed {sorted(got)}, expected {sorted(want)} (one per line)"

@task("4 bash users")
def _():
    answer(4)
    for seed in (7, 8):
        text = make_passwd(seed)
        r, _ = run(4, cwd=sandbox({"passwd.txt": text}))
        want = [f[0] for f in rows(text) if f[6] == "/bin/bash"]
        assert lines(r) == want, f"printed {lines(r)}, expected {want}"

@task("5 human accounts")
def _():
    answer(5)
    for seed in (7, 9):
        text = make_passwd(seed)
        r, _ = run(5, cwd=sandbox({"passwd.txt": text}))
        want = [f"{f[0]} {f[2]}" for f in sorted(rows(text), key=lambda f: int(f[2]))
                if 1000 <= int(f[2]) != 65534]
        assert [" ".join(l.split()) for l in lines(r)] == want, f"printed {lines(r)}, expected {want}"

@task("6 root audit")
def _():
    answer(6)
    for seed in (8, 10):
        text = make_passwd(seed)
        r, _ = run(6, cwd=sandbox({"passwd.txt": text}))
        want = [f[0] for f in rows(text) if f[2] == "0"]
        assert lines(r) == want, f"printed {lines(r)}, expected {want}"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
