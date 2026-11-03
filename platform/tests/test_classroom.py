"""Classroom mode: accounts, sessions, per-user isolation, shared-repo progress export."""

from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
CURRICULUM = Path(os.environ.get("ACADEMY_CURRICULUM", ROOT / "curriculum"))
EASY = "lls-hello"


@pytest.fixture(scope="module")
def base(tmp_path_factory):
    from academy.engine import AcademyEngine

    d = tmp_path_factory.mktemp("base")
    return AcademyEngine(CURRICULUM, d, workspace_root=d / "ws", flag_path=d / "flag.txt")


def _solution(cid: str) -> Path:
    return next(CURRICULUM.glob(f"modules/*/challenges/{cid}/solution"))


def test_password_hashing_and_sessions():
    from academy.classroom import PBKDF2_ITERATIONS, Sessions, hash_password, verify_password

    rec = hash_password("correct horse")
    assert rec["iterations"] >= 200_000 and PBKDF2_ITERATIONS >= 200_000
    assert "correct horse" not in json.dumps(rec)
    assert hash_password("correct horse")["salt"] != rec["salt"]  # salted
    assert verify_password("correct horse", rec)
    assert not verify_password("wrong horse", rec)
    assert not verify_password("x", {"salt": "zz"})

    s = Sessions()
    tok = s.create("alice")
    assert len(tok) >= 32 and s.user_for(tok) == "alice"
    assert s.user_for(tok + "x") is None and s.user_for(None) is None
    assert s.drop(tok) == "alice" and s.user_for(tok) is None


def test_sessions_survive_a_restart(tmp_path):
    from academy.classroom import Sessions

    path = tmp_path / "sessions.json"
    tok = Sessions(path=path).create("alice")
    assert tok not in path.read_text() and oct(path.stat().st_mode)[-3:] == "600"  # hashes only
    again = Sessions(path=path)
    assert again.user_for(tok) == "alice"
    again.drop(tok)
    assert Sessions(path=path).user_for(tok) is None
    expired = Sessions(ttl=-1, path=tmp_path / "old.json")
    expired.create("bob")
    assert Sessions(path=tmp_path / "old.json")._by_hash == {}


def test_autosave_goes_to_the_learners_own_folder(base, tmp_path):
    from academy.classroom import Classroom

    room = Classroom(base, tmp_path, signup=True)
    room.login("dana", "danapass1", "1.1.1.1", create=True)
    room.ctx("dana").engine.start_challenge(EASY)
    saved = json.loads((tmp_path / "users" / "dana" / ".academy" / "progress.json").read_text())
    assert EASY in saved["challenges"]
    # A new server process (same data folder) sees the same progress.
    assert EASY in Classroom(base, tmp_path).ctx("dana").engine.progress().challenges


def test_login_signup_rate_limit_and_users_file(base, tmp_path):
    from academy.classroom import Classroom

    room = Classroom(base, tmp_path, signup=True)
    assert room.login("Bad Name!", "whatever12", "1.1.1.1", create=True)[0] == 400
    assert room.login("alice", "short", "1.1.1.1", create=True)[0] == 400
    # Logging in to a name nobody created is refused: a typo never starts a fresh, empty account.
    assert room.login("zed", "zedpass12", "1.1.1.1")[0] == 401
    assert not (tmp_path / "users" / "zed").exists()
    code, body, tok = room.login("Alice", "alicepass1", "1.1.1.1", create=True)
    assert code == 200 and body == {"ok": True, "user": "alice", "created": True} and tok
    assert room.login("alice", "otherpass1", "1.1.1.1", create=True)[0] == 409  # taken
    code, body, _ = room.login("alice", "alicepass1", "1.1.1.1")
    assert code == 200 and body["created"] is False
    assert room.login("alice", "nope-nope", "1.1.1.1")[0] == 401
    raw = (tmp_path / "users.json").read_text()
    assert "alicepass1" not in raw and oct((tmp_path / "users.json").stat().st_mode)[-3:] == "600"
    # Every learner's folder, and the folders above it, are private to the server's OS account.
    for d in (tmp_path, tmp_path / "users", tmp_path / "users" / "alice"):
        assert oct(d.stat().st_mode)[-3:] == "700", d

    closed = Classroom(base, tmp_path, signup=False)
    assert closed.login("mallory", "mallorypass", "2.2.2.2", create=True)[0] == 403
    assert closed.login("mallory", "mallorypass", "2.2.2.2")[0] == 401
    assert not (tmp_path / "users" / "mallory").exists()

    codes = [room.login("alice", f"guess-{i}", "3.3.3.3")[0] for i in range(9)]
    assert codes[:7] == [401] * 7 and codes[-1] == 429
    assert room.login("alice", "alicepass1", "3.3.3.3")[0] == 429  # locked for the window


def test_two_users_are_isolated(base, tmp_path, monkeypatch):
    from academy.api import _run_workspace_check
    from academy.classroom import Classroom

    # Bogus process-global env must not leak into per-user paths.
    monkeypatch.setenv("ACADEMY_WORKSPACE", str(tmp_path / "WRONG-ws"))
    monkeypatch.setenv("ACADEMY_FLAG_PATH", str(tmp_path / "WRONG-flag.txt"))
    monkeypatch.setenv("ACADEMY_DATA", str(tmp_path / "WRONG-data"))
    room = Classroom(base, tmp_path, signup=True)
    a, b = room.ctx("alice"), room.ctx("bob")
    assert a.workspace != b.workspace and a.engine.data_dir != b.engine.data_dir

    results: dict[str, Path] = {}
    threads = [threading.Thread(target=lambda c=c: results.__setitem__(c.name, c.engine.start_challenge(EASY))) for c in (a, b)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    assert results == {"alice": a.workspace, "bob": b.workspace}

    shutil.copytree(_solution(EASY), a.workspace, dirs_exist_ok=True)
    res = _run_workspace_check(a.engine, EASY)
    assert res["ok"], res
    assert a.flag.read_text().strip() == res["flag"]
    assert not b.flag.exists()
    assert a.engine.is_solved(EASY) and not b.engine.is_solved(EASY)
    assert not _run_workspace_check(b.engine, EASY)["ok"]  # bob's own (unsolved) folder
    assert not (tmp_path / "WRONG-ws").exists() and not (tmp_path / "WRONG-flag.txt").exists()
    assert not (tmp_path / "WRONG-data").exists()


def test_progress_export_and_git_sync(base, tmp_path):
    from academy.classroom import Classroom, ProgressSync, export_progress, store_from_export

    git = lambda *a, cwd=tmp_path: subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True, text=True)  # noqa: E731
    git("init", "-q", "--bare", "-b", "main", str(tmp_path / "remote.git"))
    git("clone", "-q", str(tmp_path / "remote.git"), str(tmp_path / "clone"))
    clone = tmp_path / "clone"
    (clone / "README.md").write_text("progress\n")
    git("add", "README.md", cwd=clone)
    git("-c", "user.name=admin", "-c", "user.email=a@x", "commit", "-qm", "init", cwd=clone)
    git("push", "-q", "-u", "origin", "HEAD:main", cwd=clone)

    sync = ProgressSync(clone, start=False)
    room = Classroom(base, tmp_path / "data", sync=sync)
    a = room.ctx("alice")
    a.engine.start_challenge(EASY)
    a.engine.get_hint(EASY)
    shutil.copytree(_solution(EASY), a.workspace, dirs_exist_ok=True)
    from academy.api import _run_workspace_check

    assert _run_workspace_check(a.engine, EASY)["ok"]
    assert sync.pending["alice"]["challenges"][EASY]["solved"] is True
    assert sync.flush(sync.pending) is True

    pushed = git("--git-dir", str(tmp_path / "remote.git"), "show", "main:progress/alice.json").stdout
    data = json.loads(pushed)
    entry = data["challenges"][EASY]
    assert data["user"] == "alice" and data["solved"] == 1
    assert set(entry) == {"solved", "started_at", "completed_at", "hints_revealed", "attempts"}
    assert entry["hints_revealed"] == 1 and entry["attempts"] >= 1
    assert "flag{" not in pushed and str(tmp_path) not in pushed and "workspace" not in pushed
    author = git("--git-dir", str(tmp_path / "remote.git"), "log", "-1", "--format=%an <%ae>", "main").stdout.strip()
    assert author == "alice <alice@academy.local>"

    # Restore: same user on a fresh server data dir gets their progress back from the repo.
    room2 = Classroom(base, tmp_path / "data2", sync=sync)
    assert room2.ctx("alice").engine.is_solved(EASY)
    assert store_from_export({"user": "eve", "challenges": {}}, "alice") is None  # wrong owner
    assert store_from_export(export_progress("x", a.engine.progress()), "x").challenges[EASY].solved


def test_git_sync_into_empty_remote(base, tmp_path):
    from academy.classroom import Classroom, ProgressSync

    git = lambda *a, cwd=tmp_path: subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True, text=True)  # noqa: E731
    git("init", "-q", "--bare", "-b", "main", str(tmp_path / "remote.git"))
    git("clone", "-q", str(tmp_path / "remote.git"), str(tmp_path / "clone"))  # empty, like a new GitHub repo
    sync = ProgressSync(tmp_path / "clone", start=False)
    room = Classroom(base, tmp_path / "data", sync=sync)
    room.ctx("bob").engine.start_challenge(EASY)
    assert sync.flush(sync.pending) is True
    assert "bob" in git("--git-dir", str(tmp_path / "remote.git"), "show", "main:progress/bob.json").stdout


def test_http_requires_login(base, tmp_path):
    from academy.api import serve_api
    from academy.classroom import Classroom

    room = Classroom(base, tmp_path, signup=True)
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    threading.Thread(target=serve_api, args=(CURRICULUM, tmp_path), daemon=True,
                     kwargs={"host": "127.0.0.1", "port": port, "classroom": room, "base_engine": base}).start()
    url = f"http://127.0.0.1:{port}"
    for _ in range(50):
        try:
            urllib.request.urlopen(url + "/", timeout=1)
            break
        except OSError:
            time.sleep(0.1)

    def call(path, body=None, cookie=None):
        req = urllib.request.Request(url + path, data=None if body is None else json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json", **({"Cookie": cookie} if cookie else {})})
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                return r.status, json.loads(r.read()), r.headers.get("Set-Cookie")
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read()), None

    assert call("/api/status")[0] == 401
    assert call("/api/challenges/x/start", {})[0] == 401
    assert call("/api/login", {"username": "carol", "password": "carolpass1"})[0] == 401  # no account yet
    code, body, set_cookie = call("/api/login", {"username": "carol", "password": "carolpass1", "create": True})
    assert code == 200 and "HttpOnly" in set_cookie and "SameSite=Strict" in set_cookie
    cookie = set_cookie.split(";")[0]
    code, me, _ = call("/api/me", cookie=cookie)
    assert code == 200 and me["user"] == "carol"
    code, docs, _ = call(f"/api/challenges/{EASY}/docs", cookie=cookie)
    assert code == 200 and [d["kind"] for d in docs["docs"]] == ["readme", "lesson"]
    code, started, _ = call(f"/api/challenges/{EASY}/start", {}, cookie=cookie)
    assert code == 200 and started["workspace"].endswith("users/carol/challenge")
    assert started["terminal"] is None or "ok" in started["terminal"]
    with urllib.request.urlopen(urllib.request.Request(url + "/api/save", headers={"Cookie": cookie}), timeout=10) as r:
        assert r.headers["Content-Type"] == "application/zip" and r.read(2) == b"PK"
    try:  # learners cannot restore (it would let them mark challenges solved)
        urllib.request.urlopen(urllib.request.Request(url + "/api/restore", data=b"PK", headers={"Cookie": cookie}), timeout=10)
        raise AssertionError("restore should be refused in a classroom")
    except urllib.error.HTTPError as e:
        assert e.code == 403
    assert call("/api/logout", {}, cookie=cookie)[0] == 200
    assert call("/api/status", cookie=cookie)[0] == 401



def test_learner_gets_a_short_link_to_their_folder(base, tmp_path, monkeypatch):
    """~/signal-dojo/<name> points at users/<name>/challenge, so a learner on a laptop (WSL) finds it."""
    from academy.classroom import Classroom

    home = tmp_path / "home"
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("ACADEMY_WORKSPACE_LINKS", "1")
    (home / "signal-dojo" / "bob").mkdir(parents=True)  # a real folder is never replaced
    room = Classroom(base, tmp_path / "room", signup=True)
    alice, bob = room.ctx("alice"), room.ctx("bob")
    assert alice.engine.workspace_link == "~/signal-dojo/alice"
    assert (home / "signal-dojo" / "alice").resolve() == alice.workspace.resolve()
    assert bob.engine.workspace_link is None and not (home / "signal-dojo" / "bob").is_symlink()
    alice.engine.start_challenge(EASY)
    assert (home / "signal-dojo" / "alice" / "README.md").is_file()
