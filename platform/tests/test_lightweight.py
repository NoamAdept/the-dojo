"""The server stays light on a Raspberry Pi and on the lab network (5 learners at once)."""

from __future__ import annotations

import gzip
import http.client
import json
import os
import re
import socket
import threading
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CURRICULUM = Path(os.environ.get("ACADEMY_CURRICULUM", ROOT / "curriculum"))
STATIC = ROOT / "platform/academy/static"


def _serve(tmp_path, **kwargs) -> int:
    from academy.api import serve_api

    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    threading.Thread(target=serve_api, args=(CURRICULUM, tmp_path / "data"), daemon=True,
                     kwargs={"host": "127.0.0.1", "port": port, **kwargs}).start()
    for _ in range(100):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=1)
            return port
        except OSError:
            time.sleep(0.05)
    raise AssertionError("server did not start")


def test_page_is_compressed_cached_and_kept_alive(tmp_path):
    port = _serve(tmp_path)
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    conn.request("GET", "/", headers={"Accept-Encoding": "gzip"})
    r = conn.getresponse()
    body = r.read()
    assert r.status == 200 and r.headers["Content-Encoding"] == "gzip"
    page = (STATIC / "dojo.html").read_bytes()
    assert gzip.decompress(body) == page and len(body) < len(page) / 3
    etag = r.headers["ETag"]
    # Same connection (keep-alive): a reload costs a 304 with no body.
    conn.request("GET", "/", headers={"Accept-Encoding": "gzip", "If-None-Match": etag})
    r = conn.getresponse()
    assert r.status == 304 and r.read() == b""
    # Fonts and belts are cached by the browser for a week.
    for path in ("/fonts/Geist-400.woff2", "/icons/belt-blue.svg"):
        conn.request("GET", path)
        r = conn.getresponse()
        r.read()
        assert r.status == 200 and "max-age=604800" in r.headers["Cache-Control"], path
    conn.request("GET", "/api/modules", headers={"Accept-Encoding": "gzip"})
    r = conn.getresponse()
    assert r.headers["Content-Encoding"] == "gzip" and json.loads(gzip.decompress(r.read()))
    conn.close()


def test_belts_are_small_vector_icons():
    html = (STATIC / "dojo.html").read_text(encoding="utf-8")
    assert not re.search(r"/icons/[^\"'`]*\.png", html)
    for belt in ("white", "yellow", "orange", "green", "blue"):
        svg = (STATIC / "icons" / f"belt-{belt}.svg").read_text(encoding="utf-8")
        assert svg.startswith("<svg") and 'viewBox="0 0 64 64"' in svg and len(svg) < 2000
    assert not list((STATIC / "icons").glob("belt-*.png"))


def test_five_learners_at_once(tmp_path):
    from academy.classroom import Classroom
    from academy.engine import AcademyEngine

    data = tmp_path / "data"
    base = AcademyEngine(CURRICULUM, data, workspace_root=data / "users", flag_path=data / "unused.txt")
    room = Classroom(base, data)
    port = _serve(tmp_path, classroom=room, base_engine=base)
    names = ["ana", "ben", "cai", "dov", "eli"]

    def learner(name: str) -> dict:
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=30)
        hdr = {"Content-Type": "application/json"}
        conn.request("POST", "/api/login", json.dumps({"username": name, "password": name * 3, "create": True}), hdr)
        r = conn.getresponse()
        r.read()
        assert r.status == 200, name
        hdr["Cookie"] = r.headers["Set-Cookie"].split(";")[0]
        conn.request("POST", "/api/challenges/lls-hello/start", "{}", hdr)
        r = conn.getresponse()
        r.read()
        assert r.status == 200
        for path in ("/api/status", "/api/dojos", "/api/profile"):
            conn.request("GET", path, headers=hdr)
            r = conn.getresponse()
            r.read()
            assert r.status == 200
        conn.request("GET", "/api/me", headers=hdr)
        me = json.loads(conn.getresponse().read())
        conn.close()
        return me

    with ThreadPoolExecutor(5) as pool:
        mes = list(pool.map(learner, names))
    assert [m["user"] for m in mes] == names
    for name in names:
        saved = data / "users" / name / ".academy" / "progress.json"
        assert "lls-hello" in json.loads(saved.read_text())["challenges"], name
        assert (data / "users" / name / "challenge").is_dir()


def test_a_second_copy_on_a_taken_port_says_so(tmp_path):
    """An older Signal Dojo still on the port: run.sh stops with a plain message instead of a
    traceback, before it opens the browser on the old copy."""
    import subprocess

    import pytest

    from academy.api import check_port

    with socket.socket() as old:
        old.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        old.bind(("127.0.0.1", 0))
        old.listen()
        port = old.getsockname()[1]
        with pytest.raises(SystemExit) as e:
            check_port("127.0.0.1", port)
        assert "already in use" in str(e.value) and f"PORT={port + 1}" in str(e.value)

        env = {**os.environ, "HOME": str(tmp_path), "HOST": "127.0.0.1", "PORT": str(port),
               "OPEN_BROWSER": "0", "ACADEMY_DATA": str(tmp_path / "data")}
        r = subprocess.run([str(ROOT / "run.sh")], env=env, capture_output=True, text=True, timeout=60)
        assert r.returncode == 1
        assert "already in use" in r.stderr and "Traceback" not in r.stderr
    check_port("127.0.0.1", port)  # free again: no exit
