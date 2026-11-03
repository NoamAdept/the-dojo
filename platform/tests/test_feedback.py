"""Learner feedback after a challenge, and the hint endpoint (offline)."""

from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
CURRICULUM = ROOT / "curriculum"
CID = "zt-first-commands"


@pytest.fixture()
def engine(tmp_path):
    from academy.engine import AcademyEngine

    return AcademyEngine(curriculum_root=CURRICULUM, data_dir=tmp_path / "data", workspace_root=tmp_path / "ws")


def test_feedback_is_saved_to_jsonl(engine):
    entry = engine.record_feedback(CID, "too-hard", "  Task 3\n was   confusing ")
    assert entry["note"] == "Task 3 was confusing"
    lines = (engine.data_dir / "feedback.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    saved = json.loads(lines[0])
    assert saved["challenge"] == CID and saved["rating"] == "too-hard" and saved["title"]


def test_feedback_rating_or_note_alone_is_enough(engine):
    engine.record_feedback(CID, "about-right", "")
    engine.record_feedback(CID, "", "typo in task 2")
    assert [e["rating"] for e in engine.feedback()] == ["", "about-right"]  # newest first


@pytest.mark.parametrize("rating, note", [("", ""), ("", "   "), ("great", ""), ("TOO-HARD", "x")])
def test_feedback_rejects_empty_or_unknown_rating(engine, rating, note):
    with pytest.raises(ValueError):
        engine.record_feedback(CID, rating, note)
    assert not (engine.data_dir / "feedback.jsonl").exists()


def test_feedback_unknown_challenge(engine):
    with pytest.raises(KeyError):
        engine.record_feedback("no-such-challenge", "too-easy", "")


def test_feedback_note_is_capped_and_bad_lines_skipped(engine):
    engine.record_feedback(CID, "", "x" * 5000)
    with (engine.data_dir / "feedback.jsonl").open("a", encoding="utf-8") as fh:
        fh.write("not json\n")
    entries = engine.feedback()
    assert len(entries) == 1 and len(entries[0]["note"]) == 1000


def test_feedback_goes_into_the_save_file(engine):
    from academy.backup import export_zip

    engine.record_feedback(CID, "too-easy", "")
    buf = io.BytesIO()
    export_zip(engine.data_dir, buf, name="Ada")
    assert "feedback.jsonl" in zipfile.ZipFile(io.BytesIO(buf.getvalue())).namelist()


def test_http_hint_and_feedback(engine):
    import socket
    import threading
    import time
    import urllib.error
    import urllib.request

    from academy.api import serve_api

    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    threading.Thread(target=serve_api, args=(CURRICULUM, engine.data_dir), daemon=True,
                     kwargs={"host": "127.0.0.1", "port": port, "base_engine": engine}).start()
    url = f"http://127.0.0.1:{port}"
    for _ in range(50):
        try:
            urllib.request.urlopen(url + "/api/status", timeout=1)
            break
        except OSError:
            time.sleep(0.1)

    def post(path, body):
        req = urllib.request.Request(url + path, data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())

    # Pressing Hint many times never goes past the last hint, and every reply lists all hints shown so far.
    total = len(engine.get_challenge(CID).hints)
    replies = [post(f"/api/challenges/{CID}/hint", {}) for _ in range(total + 3)]
    assert [r["level"] for r in replies] == list(range(1, total + 1)) + [total] * 3
    assert [len(r["hints"]) for r in replies] == list(range(1, total + 1)) + [total] * 3
    assert all(r["total"] == total for r in replies)

    assert post(f"/api/challenges/{CID}/feedback", {"rating": "about-right", "note": "fine"}) == {"ok": True}
    assert engine.feedback()[0]["note"] == "fine"
    for path, body, code in [
        (f"/api/challenges/{CID}/feedback", {}, 400),
        (f"/api/challenges/{CID}/feedback", {"rating": "meh"}, 400),
        ("/api/challenges/no-such-challenge/feedback", {"rating": "too-easy"}, 404),
    ]:
        with pytest.raises(urllib.error.HTTPError) as err:
            post(path, body)
        assert err.value.code == code
    assert len(engine.feedback()) == 1
