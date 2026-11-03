"""Save / restore: progress and the learner's own files in one .zip (offline)."""

from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
CURRICULUM = ROOT / "curriculum"
A, B = "zt-first-commands", "zt-vim-cat"  # no prerequisites


def _engine(tmp_path: Path, name: str):
    from academy.engine import AcademyEngine

    return AcademyEngine(
        curriculum_root=CURRICULUM, data_dir=tmp_path / name / "data", workspace_root=tmp_path / name / "ws"
    )


@pytest.fixture()
def engine(tmp_path):
    return _engine(tmp_path, "one")


def test_start_keeps_and_brings_back_learner_files(engine):
    ws = engine.start_challenge(B)
    (ws / "solve.sh").write_text("echo mine\n", encoding="utf-8")
    (ws / "solve.sh").chmod(0o755)
    (ws / "poem.txt").write_text("edited\n", encoding="utf-8")
    (ws / "__pycache__").mkdir()
    (ws / "__pycache__" / "x.pyc").write_bytes(b"junk")

    engine.start_challenge(A)  # wipes the folder
    assert not (ws / "solve.sh").exists()
    kept = engine.data_dir / "work" / B
    assert sorted(p.name for p in kept.iterdir()) == ["poem.txt", "solve.sh"]  # untouched starters not kept

    engine.start_challenge(B)
    assert (ws / "solve.sh").read_text(encoding="utf-8") == "echo mine\n"
    assert (ws / "solve.sh").stat().st_mode & 0o111
    assert (ws / "poem.txt").read_text(encoding="utf-8") == "edited\n"
    assert (ws / "check.py").is_file()


def test_restart_starts_clean_but_keeps_files(engine):
    ws = engine.start_challenge(B)
    (ws / "poem.txt").write_text("broken\n", encoding="utf-8")
    engine.start_challenge(B)  # Restart: fresh starter files
    assert (ws / "poem.txt").read_text(encoding="utf-8") != "broken\n"
    assert (engine.data_dir / "work" / B / "poem.txt").read_text(encoding="utf-8") == "broken\n"


def test_restarting_without_changes_keeps_earlier_files(engine):
    ws = engine.start_challenge(B)
    (ws / "notes.txt").write_text("hi\n", encoding="utf-8")
    engine.start_challenge(A)
    engine.start_challenge(A)  # nothing written for A
    assert (engine.data_dir / "work" / B / "notes.txt").is_file()
    assert not (engine.data_dir / "work" / A).exists()


def test_save_and_restore_on_another_machine(engine, tmp_path):
    from academy.progress import ChallengeProgress

    ws = engine.start_challenge(B)
    (ws / "solve.py").write_text("print('mine')\n", encoding="utf-8")  # still in the folder: Save keeps it
    store = engine.progress()
    store.challenges[A] = ChallengeProgress(solved=True, completed_at=100.0, attempts=2)
    engine.progress_repo.save(store)

    buf = io.BytesIO()
    summary = engine.save_to(buf, name="Ada")
    assert summary["solved"] == 1 and summary["challenges_with_files"] == 1
    names = zipfile.ZipFile(io.BytesIO(buf.getvalue())).namelist()
    assert f"work/{B}/solve.py" in names and "progress.json" in names

    other = _engine(tmp_path, "two")
    result = other.restore_from(buf.getvalue())
    assert result["ok"] and result["name"] == "Ada"
    assert result["solved"] == 1 and result["newly_solved"] == 1
    assert other.is_solved(A)
    ws2 = other.start_challenge(B)
    assert (ws2 / "solve.py").read_text(encoding="utf-8") == "print('mine')\n"


def test_restore_never_loses_local_progress(engine, tmp_path):
    from academy.backup import merge_progress
    from academy.progress import ChallengeProgress, ProgressStore

    local = ProgressStore(challenges={A: ChallengeProgress(solved=True, completed_at=50.0, attempts=1)})
    incoming = ProgressStore(challenges={
        A: ChallengeProgress(solved=False, attempts=4, hints_revealed=2),
        B: ChallengeProgress(solved=True, completed_at=70.0),
    })
    merged = merge_progress(local, incoming)
    assert merged.challenges[A].solved and merged.challenges[A].completed_at == 50.0
    assert merged.challenges[A].attempts == 4 and merged.challenges[A].hints_revealed == 2
    assert merged.challenges[B].solved


def _zip(entries: dict[str, bytes | str]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for name, data in entries.items():
            zf.writestr(name, data)
    return buf.getvalue()


MANIFEST = json.dumps({"format": "signal-dojo-save", "version": 1})


@pytest.mark.parametrize("payload", [
    b"not a zip",
    _zip({"progress.json": "{}"}),  # no manifest
    _zip({"signal-dojo-save.json": MANIFEST, "work/../../evil.sh": "x"}),
    _zip({"signal-dojo-save.json": MANIFEST, f"work/{A}/../../evil.sh": "x"}),
    _zip({"signal-dojo-save.json": MANIFEST, "progress.json": "[1, 2]"}),
])
def test_bad_save_files_are_refused(engine, tmp_path, payload):
    from academy.backup import SaveFileError

    with pytest.raises(SaveFileError):
        engine.restore_from(payload)
    assert not (tmp_path / "one" / "evil.sh").exists()
    assert not engine.progress_repo.path.exists()


def test_cli_save_and_restore(tmp_path, monkeypatch, capsys):
    from academy.cli import main

    for name in ("one", "two"):
        (tmp_path / name).mkdir()
    monkeypatch.setenv("ACADEMY_CURRICULUM", str(CURRICULUM))
    monkeypatch.setenv("ACADEMY_DATA", str(tmp_path / "one" / "data"))
    monkeypatch.setenv("ACADEMY_WORKSPACE", str(tmp_path / "one" / "ws"))
    assert main(["start", B]) == 0
    (tmp_path / "one" / "ws" / "mine.txt").write_text("x\n", encoding="utf-8")
    out = tmp_path / "save.zip"
    assert main(["save", str(out)]) == 0
    assert out.is_file()

    monkeypatch.setenv("ACADEMY_DATA", str(tmp_path / "two" / "data"))
    monkeypatch.setenv("ACADEMY_WORKSPACE", str(tmp_path / "two" / "ws"))
    assert main(["restore", str(out)]) == 0
    assert (tmp_path / "two" / "data" / "work" / B / "mine.txt").is_file()
    assert main(["restore", str(tmp_path / "missing.zip")]) == 1


def test_http_save_and_restore(tmp_path):
    import socket
    import threading
    import time
    import urllib.error
    import urllib.request

    from academy.api import serve_api

    eng = _engine(tmp_path, "web")
    ws = eng.start_challenge(B)
    (ws / "mine.py").write_text("x = 1\n", encoding="utf-8")
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    threading.Thread(target=serve_api, args=(CURRICULUM, eng.data_dir), daemon=True,
                     kwargs={"host": "127.0.0.1", "port": port, "base_engine": eng}).start()
    url = f"http://127.0.0.1:{port}"
    for _ in range(50):
        try:
            urllib.request.urlopen(url + "/api/status", timeout=1)
            break
        except OSError:
            time.sleep(0.1)

    with urllib.request.urlopen(url + "/api/save?name=Ada", timeout=10) as r:
        assert "attachment" in r.headers["Content-Disposition"]
        saved = r.read()
    assert f"work/{B}/mine.py" in zipfile.ZipFile(io.BytesIO(saved)).namelist()

    req = urllib.request.Request(url + "/api/restore", data=saved, headers={"Content-Type": "application/zip"})
    with urllib.request.urlopen(req, timeout=10) as r:
        body = json.loads(r.read())
    assert body["ok"] and body["name"] == "Ada" and body["challenges_with_files"] == 1

    req = urllib.request.Request(url + "/api/restore", data=b"nope", headers={"Content-Type": "application/zip"})
    with pytest.raises(urllib.error.HTTPError) as err:
        urllib.request.urlopen(req, timeout=10)
    assert err.value.code == 400 and "save file" in json.loads(err.value.read())["error"]
