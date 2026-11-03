"""Core state: progress is saved, moving between challenges keeps it, Start resets the folder."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from academy.progress import ChallengeProgress, ProgressRepository, ProgressStore

ROOT = Path(__file__).resolve().parents[2]
CURRICULUM = ROOT / "curriculum"
FIRST, SECOND = "zt-first-commands", "zt-files-folders"


@pytest.fixture()
def engine(tmp_path):
    from academy.engine import AcademyEngine

    return AcademyEngine(curriculum_root=CURRICULUM, data_dir=tmp_path / "data",
                         workspace_root=tmp_path / "ws", flag_path=tmp_path / "flag.txt")


def solve_by_check(engine, cid):
    from academy.api import _run_workspace_check

    ws = engine.start_challenge(cid)
    solve = CURRICULUM / "modules/18-zero-terminal/challenges" / cid / "solution/solve.sh"
    import subprocess
    subprocess.run(["bash", str(solve)], cwd=ws, check=True, capture_output=True)
    return _run_workspace_check(engine, cid)


def test_store_round_trips_through_json(tmp_path):
    repo = ProgressRepository(tmp_path / "progress.json")
    store = ProgressStore()
    store.start(FIRST, workspace="/w")
    store.reveal_hint(FIRST, 3)
    store.record_attempt(FIRST, False)
    store.record_attempt(FIRST, True)
    repo.save(store)
    back = repo.load()
    assert back.to_dict() == store.to_dict()
    assert back.current_challenge_id == FIRST and back.current_workspace == "/w"
    assert json.loads((tmp_path / "progress.json").read_text())["challenges"][FIRST]["solved"] is True


def test_missing_progress_file_is_a_fresh_start(tmp_path):
    store = ProgressRepository(tmp_path / "none" / "progress.json").load()
    assert store.challenges == {} and store.current_challenge_id is None


def test_solving_twice_keeps_the_first_time_and_counts_attempts():
    store = ProgressStore()
    store.record_attempt(FIRST, False)
    assert not store.challenges[FIRST].solved and store.challenges[FIRST].completed_at is None
    store.record_attempt(FIRST, True)
    first_time = store.challenges[FIRST].completed_at
    store.record_attempt(FIRST, True)
    assert store.challenges[FIRST].solved and store.challenges[FIRST].completed_at == first_time
    assert store.challenges[FIRST].attempts == 3


def test_hints_stop_at_the_last_one():
    store = ProgressStore()
    assert [store.reveal_hint(FIRST, 3) for _ in range(5)] == [1, 2, 3, 3, 3]


def test_old_progress_files_without_new_fields_still_load():
    store = ProgressStore.from_dict({"challenges": {FIRST: {"solved": True}}})
    assert store.challenges[FIRST] == ChallengeProgress(solved=True)
    assert store.student_id == "local"


def test_start_records_the_current_challenge_and_moving_on_keeps_progress(engine):
    res = solve_by_check(engine, FIRST)
    assert res["ok"], res
    engine.start_challenge(SECOND)
    store = engine.progress()
    assert store.current_challenge_id == SECOND
    assert store.challenges[FIRST].solved and not store.challenges[SECOND].solved
    assert (engine.workspace_root / ".challenge").read_text().strip() == SECOND
    assert not (engine.workspace_root / "hello.txt").exists(), "the first challenge's files must leave the folder"


def test_next_available_moves_forward_after_a_solve(engine):
    assert engine.next_available_challenge().id == FIRST
    assert solve_by_check(engine, FIRST)["ok"]
    assert engine.next_available_challenge().id == SECOND


def test_failed_check_does_not_solve(engine):
    from academy.api import _run_workspace_check

    engine.start_challenge(FIRST)
    res = _run_workspace_check(engine, FIRST)
    assert not res["ok"] and "hello.txt" in res["detail"]
    assert not engine.is_solved(FIRST)


def test_check_refuses_a_challenge_that_was_not_started(engine):
    from academy.api import _run_workspace_check

    engine.start_challenge(FIRST)
    res = _run_workspace_check(engine, SECOND)
    assert not res["ok"] and "Start this challenge first" in res["error"]


def test_restart_gives_clean_starter_files(engine):
    ws = engine.start_challenge(FIRST)
    (ws / "README.md").write_text("scribbled over\n")
    (ws / "hello.txt").write_text("Hello terminal\n")
    ws = engine.start_challenge(FIRST)
    starter = (CURRICULUM / "modules/18-zero-terminal/challenges" / FIRST / "files/README.md").read_text()
    assert (ws / "README.md").read_text() == starter
    assert not (ws / "hello.txt").exists()


def test_progress_survives_a_new_engine(engine, tmp_path):
    from academy.engine import AcademyEngine

    assert solve_by_check(engine, FIRST)["ok"]
    again = AcademyEngine(curriculum_root=CURRICULUM, data_dir=tmp_path / "data",
                          workspace_root=tmp_path / "ws", flag_path=tmp_path / "flag.txt")
    assert again.is_solved(FIRST)
    assert again.status_summary()["solved"] == 1


def test_staging_never_copies_bytecode(engine, tmp_path):
    cache = CURRICULUM / "modules/18-zero-terminal/challenges" / FIRST / "files/__pycache__"
    made = not cache.exists()  # running ./check in the curriculum folder can leave one behind
    cache.mkdir(exist_ok=True)
    stale = cache / "test-stale.cpython-313.pyc"
    stale.write_bytes(b"stale")
    try:
        ws = engine.start_challenge(FIRST)
        assert not (ws / "__pycache__").exists()
    finally:
        stale.unlink()
        if made:
            cache.rmdir()
