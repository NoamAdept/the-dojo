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

import random, signal, socket, sys, time, urllib.request

RNG = random.Random(43121)
GROUPS = []          # process groups started for a task; all killed in cleanup()
NOPROXY = urllib.request.build_opener(urllib.request.ProxyHandler({}))
ENV = {"no_proxy": "127.0.0.1,localhost", "NO_PROXY": "127.0.0.1,localhost"}

CTL = """#!/bin/bash
# Tiny service controller: ./ctl.sh start|stop|restart
cd "$(dirname "$0")"
case "$1" in
  start)
    port=$(grep '^port=' beacon.conf | cut -d= -f2)
    echo "$(date '+%F %T') INFO starting on port $port" >> beacon.log
    python3 -m http.server "$port" --bind 127.0.0.1 >> beacon.log 2>&1 &
    echo $! > beacon.pid
    sleep 1
    echo "started on port $port"
    ;;
  stop)
    [ -f beacon.pid ] && kill "$(cat beacon.pid)" 2>/dev/null
    rm -f beacon.pid
    sleep 0.5
    echo "stopped"
    ;;
  restart)
    "$0" stop
    "$0" start
    ;;
  *)
    echo "usage: $0 start|stop|restart"
    exit 1
    ;;
esac
"""

def free_port(taken=()):
    while True:
        p = RNG.randint(20000, 60999)
        if p in taken:
            continue
        with socket.socket() as s:
            try:
                s.bind(("127.0.0.1", p))
                return p
            except OSError:
                pass

def answers_on(port):
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=0.3):
            return True
    except OSError:
        return False

def wait_for(port, up=True, secs=8):
    end = time.time() + secs
    while time.time() < end:
        if answers_on(port) == up:
            return True
        time.sleep(0.1)
    return False

def fetch(port, path):
    with NOPROXY.open(f"http://127.0.0.1:{port}{path}", timeout=3) as r:
        return r.read().decode()

def serve(d, port):
    """Start a helper http.server sharing folder d."""
    p = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"], cwd=d,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    GROUPS.append(p.pid)
    if not wait_for(port):
        raise RuntimeError("./check could not start its helper server")

def go(n, d):
    """Run answers/taskN.sh in its own process group; output goes to files so a forgotten & cannot hang us."""
    out, err = (tempfile.TemporaryFile("w+") for _ in range(2))
    p = subprocess.Popen(["bash", str(answer(n))], cwd=d, stdout=out, stderr=err, start_new_session=True,
                         env={**os.environ, "HOME": str(d), **ENV})
    GROUPS.append(p.pid)
    try:
        p.wait(timeout=20)
    except subprocess.TimeoutExpired:
        raise AssertionError("your script did not finish within 20 seconds. Did you forget the & at the end of the server line, or the > server.log 2>&1 part?")
    out.seek(0)
    return out.read()

def is_server(pid):
    try:
        return b"http.server" in pathlib.Path(f"/proc/{pid}/cmdline").read_bytes()
    except (OSError, ValueError):
        return False

def cleanup(d):
    for g in GROUPS:
        try:
            os.killpg(g, signal.SIGKILL)
        except OSError:
            pass
    GROUPS.clear()
    for pf in d.glob("*.pid"):   # a server started with setsid escapes the group; its PID file finds it
        pid = pf.read_text().strip()
        if pid.isdigit() and is_server(int(pid)):
            try:
                os.kill(int(pid), signal.SIGKILL)
            except OSError:
                pass

def listen_addrs(port):
    """Local addresses listening on port, read from /proc (Linux)."""
    found = []
    for f in ("/proc/net/tcp", "/proc/net/tcp6"):
        try:
            rows = open(f).read().splitlines()[1:]
        except OSError:
            continue
        for row in rows:
            col = row.split()
            addr, hexport = col[1].split(":")
            if col[3] == "0A" and int(hexport, 16) == port:
                found.append(addr)
    return found

@task("1 start a server in the background")
def _():
    answer(1)
    port, token = free_port(), "hello-%06d" % RNG.randint(0, 999999)
    d = sandbox({"port.txt": f"{port}\n", "hello.txt": token + "\n"})
    try:
        go(1, d)
        assert wait_for(port), f"nothing answers on port {port}. Start python3 -m http.server with the port from port.txt, and end the line with & so it keeps running in the background"
        assert fetch(port, "/hello.txt").strip() == token, "the server answers, but not with this folder's hello.txt. Start it from the current folder."
        addrs = listen_addrs(port)
        assert all(a == "0100007F" for a in addrs), "the server listens on every network connection, not just localhost. Add --bind 127.0.0.1"
        pf = d / "server.pid"
        assert pf.exists(), "write the server's PID to server.pid (echo $! > server.pid right after the & line)"
        pid = pf.read_text().strip()
        assert pid.isdigit() and is_server(int(pid)), f"server.pid holds {pid!r}, which is not the PID of the running server. Use $! right after the & line."
        assert (d / "server.log").exists(), "send the server's output to server.log (> server.log 2>&1)"
    finally:
        cleanup(d)

@task("2 ask it something with curl")
def _():
    answer(2)
    port, token = free_port(), "status-%06d" % RNG.randint(0, 999999)
    www = sandbox({"status.txt": f"radio ok {token}\n"})
    d = sandbox({"port.txt": f"{port}\n"})
    try:
        serve(www, port)
        out = go(2, d)
        assert token in out, f"your output {out.strip()!r} does not contain the server's /status.txt. Try: curl -s http://127.0.0.1:PORT/status.txt"
    finally:
        cleanup(d)

@task("3 which port answers?")
def _():
    answer(3)
    # The live port sits on a different line each round, so always printing the same line can't pass.
    for at in RNG.sample(range(4), 2):
        ports = []
        for _ in range(4):
            ports.append(free_port(ports))
        live = ports[at]
        d = sandbox({"ports.txt": "".join(f"{p}\n" for p in ports)})
        try:
            serve(sandbox(), live)
            out = go(3, d).strip().splitlines()
            assert out[-1:] == [str(live)], f"printed {out}, but the server is on {live}. Try each port with curl and print the one that works."
        finally:
            cleanup(d)

@task("4 read the log")
def _():
    answer(4)
    for _round in range(2):
        ports = [free_port() for _ in range(3)]
        log = []
        for i, p in enumerate(ports):
            t = f"2026-10-06 10:{10 + i * 7:02d}:0{i}"
            log.append(f"{t} INFO starting beacon")
            if i < 2:
                log.append(f"{t} INFO listening on 127.0.0.1:{p}")
                log.append(f"{t} ERROR lost connection to radio on port {RNG.randint(1000, 9999)}")
                log.append(f"{t} INFO shutting down")
            else:
                log.append(f"{t} INFO listening on 127.0.0.1:{p}")
                log.append(f"{t} INFO GET /status 200")
        d = sandbox({"service.log": "\n".join(log) + "\n"})
        out = go(4, d).strip().splitlines()
        assert out[-1:] == [str(ports[-1])], f"printed {out}, expected {ports[-1]} (from the last 'listening on' line)"

@task("5 edit the config and restart")
def _():
    answer(5)
    old = free_port()
    new = free_port([old])
    conf = f"# beacon settings\nname=beacon\nport={old}\nmessage=hello\n"
    d = sandbox({"beacon.conf": conf, "ctl.sh": CTL, "new_port.txt": f"{new}\n", "hello.txt": "beacon\n"})
    (d / "ctl.sh").chmod(0o755)
    try:
        p = subprocess.Popen(["bash", "ctl.sh", "start"], cwd=d, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        GROUPS.append(p.pid)
        p.wait(timeout=20)
        if not wait_for(old):
            raise RuntimeError("./check could not start the beacon service")
        go(5, d)
        want = conf.replace(f"port={old}", f"port={new}")
        assert (d / "beacon.conf").read_text() == want, f"beacon.conf should only have its port= line changed to port={new}. It now reads: {(d / 'beacon.conf').read_text()!r}"
        assert wait_for(new), f"nothing answers on the new port {new}. Editing the config is not enough: restart the service (./ctl.sh restart)."
        assert wait_for(old, up=False, secs=3), f"the old server still answers on port {old}. Stop it before starting the new one (./ctl.sh restart does both)."
    finally:
        cleanup(d)

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
