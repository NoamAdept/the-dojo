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

import random, signal, sys, time

RNG = random.Random(4242)
KIDS = []
CHILD = """
import pathlib, signal, sys, time
d = pathlib.Path(sys.argv[2])
def on_int(*a):
    (d / (sys.argv[1] + ".int")).write_text("interrupted")
    sys.exit(0)
signal.signal(signal.SIGINT, on_int)
(d / (sys.argv[1] + ".ready")).write_text("ok")
while True:
    time.sleep(0.05)
"""

def word():
    return "beacon-" + "".join(RNG.choice("abcdefghjkmnpqrstuvwxyz") for _ in range(6))

def spawn(marker, d):
    """Start a harmless helper with marker in its command line; wait until it is ready."""
    p = subprocess.Popen([sys.executable, "-c", CHILD, marker, str(d)], start_new_session=True)
    KIDS.append(p)
    for _ in range(100):
        if (d / (marker + ".ready")).exists():
            return p
        time.sleep(0.05)
    raise RuntimeError("helper process did not start")

def cleanup():
    for p in KIDS:
        if p.poll() is None:
            try:
                os.kill(p.pid, signal.SIGCONT)
            except OSError:
                pass
            p.kill()
        p.wait()
    KIDS.clear()

def state(pid):
    return open(f"/proc/{pid}/stat").read().rsplit(")", 1)[1].split()[0]

def target_and_decoys():
    names = [word() for _ in range(3)]
    d = sandbox({"target.txt": names[0] + "\n"})
    procs = [spawn(n, d) for n in names]
    return d, procs[0], procs[1:]

@task("1 find a PID")
def _():
    answer(1)
    try:
        d, target, _decoys = target_and_decoys()
        r, _ = run(1, cwd=d)
        assert r.stdout.strip() == str(target.pid), f"printed {r.stdout.strip()!r}, the target PID is {target.pid}"
    finally:
        cleanup()

@task("2 kill the right process")
def _():
    answer(2)
    try:
        d, target, decoys = target_and_decoys()
        run(2, cwd=d)
        try:
            target.wait(timeout=3)
        except subprocess.TimeoutExpired:
            raise AssertionError("the target process is still running")
        assert all(p.poll() is None for p in decoys), "you also ended a decoy (a process that only looks similar). Match the exact word"
    finally:
        cleanup()

@task("3 interrupt with SIGINT")
def _():
    answer(3)
    try:
        d = sandbox()
        m = word()
        p = spawn(m, d)
        (d / "pid.txt").write_text(f"{p.pid}\n")
        run(3, cwd=d)
        for _ in range(60):
            if (d / (m + ".int")).exists():
                break
            time.sleep(0.05)
        else:
            raise AssertionError("the process never received SIGINT (the Ctrl-C signal)")
    finally:
        cleanup()

@task("4 suspend and resume")
def _():
    answer(4)
    try:
        d = sandbox()
        p = spawn(word(), d)
        (d / "pid.txt").write_text(f"{p.pid}\n")
        run(4, cwd=d)
        st = d / "state.txt"
        assert st.exists(), "write the stopped state to state.txt"
        assert st.read_text().strip().startswith("T"), f"state.txt says {st.read_text().strip()!r}. A stopped process shows T"
        time.sleep(0.2)
        assert p.poll() is None, "the process should still be alive"
        assert state(p.pid) in "RS", "the process is still stopped. Send it CONT"
    finally:
        cleanup()

@task("5 background and wait")
def _():
    answer(5)
    # slow.sh lets go of the script's output, so the script ends when it ends, not when the jobs do.
    d = sandbox({"slow.sh": "#!/bin/bash\nexec >/dev/null 2>&1\nsleep 1\necho \"$1\" >> log.txt\n"})
    (d / "slow.sh").chmod(0o755)
    t = time.time()
    r, _ = run(5, cwd=d)
    took = time.time() - t
    log = (d / "log.txt").read_text().split() if (d / "log.txt").exists() else []
    assert sorted(log) == ["A", "B"], f"log.txt has {log}. Did you wait for both jobs?"
    assert took < 1.8, f"took {took:.1f} s. Run both in the background with &"
    assert r.stdout.strip().splitlines()[-1:] == ["done"], "print done after both finish"

@task("6 exit codes")
def _():
    answer(6)
    for code in (RNG.randint(2, 60), RNG.randint(61, 120)):
        d = sandbox({"mystery": f"#!/bin/bash\necho working...\nexit {code}\n"})
        (d / "mystery").chmod(0o755)
        r, _ = run(6, cwd=d)
        last = r.stdout.strip().splitlines()[-1:]
        assert last == [str(code)], f"last line is {last}, but mystery exited with {code}"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
