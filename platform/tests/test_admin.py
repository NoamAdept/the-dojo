"""Tests for curriculum admin helpers."""

from __future__ import annotations

import os
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
CURRICULUM = ROOT / "curriculum"


@pytest.fixture()
def engine(tmp_path):
    from academy.engine import AcademyEngine

    ws = tmp_path / "workspace"
    data = tmp_path / "data"
    return AcademyEngine(curriculum_root=CURRICULUM, data_dir=data, workspace_root=ws)


@pytest.fixture()
def sandbox_curriculum(tmp_path):
    """Minimal curriculum tree for write tests."""
    mod_dir = tmp_path / "modules" / "99-test-admin"
    ch_root = mod_dir / "challenges"
    mod_dir.mkdir(parents=True)
    (mod_dir / "module.yaml").write_text(
        yaml.safe_dump(
            {
                "id": "test-admin",
                "slug": "test-admin",
                "title": "Admin Test Module",
                "order": 99,
                "description": "Temporary module for admin tests.\n",
                "prerequisites": [],
                "challenges": [],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    ch_root.mkdir()
    return tmp_path


@pytest.fixture(autouse=True)
def admin_data(tmp_path, monkeypatch):
    """Each test gets its own admin.json and starts locked."""
    monkeypatch.setenv("ACADEMY_DATA", str(tmp_path / "admin-data"))
    monkeypatch.delenv("ACADEMY_ADMIN_UNLOCK", raising=False)


def _unlock_admin(monkeypatch):
    from academy import admin_auth

    if not admin_auth.has_password():
        admin_auth.set_password("correct horse")
    monkeypatch.setenv("ACADEMY_ADMIN", "1")
    assert admin_auth.check_password("correct horse")
    admin_auth.unlock()


def test_admin_enabled_env(monkeypatch):
    from academy.admin import admin_enabled

    monkeypatch.delenv("ACADEMY_ADMIN", raising=False)
    assert admin_enabled() is False
    monkeypatch.setenv("ACADEMY_ADMIN", "1")
    assert admin_enabled() is False, "the env var alone must not turn admin mode on"
    _unlock_admin(monkeypatch)
    assert admin_enabled() is True


def test_admin_password_hash_and_unlock(monkeypatch):
    from academy import admin_auth

    assert not admin_auth.has_password()
    with pytest.raises(ValueError):
        admin_auth.set_password("short")
    path = admin_auth.set_password("correct horse")
    record = path.read_text()
    assert "correct horse" not in record and '"salt"' in record
    assert oct(path.stat().st_mode & 0o777) == "0o600"
    assert admin_auth.check_password("correct horse")
    assert not admin_auth.check_password("wrong horse")

    monkeypatch.setenv("ACADEMY_ADMIN_UNLOCK", "forged")
    assert not admin_auth.is_unlocked()
    admin_auth.unlock()
    assert admin_auth.is_unlocked()

    admin_auth.set_password("another horse")  # a new password invalidates old unlocks
    assert not admin_auth.is_unlocked()
    assert admin_auth.reset_password() and not admin_auth.has_password()


def test_admin_cli_refuses_without_terminal(monkeypatch, capsys):
    from academy import admin_auth
    from academy.cli import main

    admin_auth.set_password("correct horse")
    monkeypatch.setenv("ACADEMY_ADMIN", "1")
    monkeypatch.setattr(admin_auth, "_interactive", lambda: False)
    assert main(["start", "pyq-generics"]) == 1
    assert main(["admin"]) == 1
    assert "admin password" in capsys.readouterr().err


def test_admin_cli_asks_for_password(monkeypatch):
    from academy import admin_auth

    admin_auth.set_password("correct horse")
    monkeypatch.setattr(admin_auth, "_interactive", lambda: True)
    answers = iter(["nope", "correct horse"])
    monkeypatch.setattr(admin_auth.getpass, "getpass", lambda _prompt="": next(answers))
    assert admin_auth.require_admin() is True
    assert admin_auth.is_unlocked()


def test_first_run_sets_password(monkeypatch):
    from academy import admin_auth

    monkeypatch.setattr(admin_auth, "_interactive", lambda: True)
    answers = iter(["correct horse", "correct horse"])
    monkeypatch.setattr(admin_auth.getpass, "getpass", lambda _prompt="": next(answers))
    admin_auth.first_run_setup()
    assert admin_auth.check_password("correct horse")
    admin_auth.first_run_setup()  # already set: no prompt (iterator is empty)


def test_first_run_skip_is_remembered(monkeypatch):
    from academy import admin_auth

    monkeypatch.setattr(admin_auth, "_interactive", lambda: True)
    answers = iter([""])
    monkeypatch.setattr(admin_auth.getpass, "getpass", lambda _prompt="": next(answers))
    admin_auth.first_run_setup()
    assert not admin_auth.has_password() and admin_auth.setup_skipped()
    admin_auth.first_run_setup()  # skipped once: never nags again


def test_validate_challenge_draft_requires_hints():
    from academy.admin import default_challenge_draft, validate_challenge_draft

    draft = default_challenge_draft("orientation", "Sample")
    draft["hints"] = [{"level": 1, "text": "only one"}]
    errors = validate_challenge_draft(draft)
    assert any("two hints" in e.lower() for e in errors)


def test_build_and_validate_default_draft():
    from academy.admin import build_challenge_yaml, default_challenge_draft, validate_challenge_draft

    draft = default_challenge_draft("orientation", "Filesystem Warmup")
    normalized = build_challenge_yaml(draft)
    errors = validate_challenge_draft(normalized)
    assert errors == []
    assert normalized["id"].startswith("orientation-")


def test_create_challenge_writes_files(sandbox_curriculum):
    from academy.admin import create_challenge, default_challenge_draft
    from academy.engine import AcademyEngine

    engine = AcademyEngine(curriculum_root=sandbox_curriculum, data_dir=sandbox_curriculum / "data")
    draft = default_challenge_draft("test-admin", "Probe Challenge")
    draft["id"] = "test-admin-probe-challenge"
    draft["title"] = "Probe Challenge"

    result = create_challenge(engine, draft)
    assert result["ok"] is True

    ch_dir = sandbox_curriculum / "modules" / "99-test-admin" / "challenges" / "test-admin-probe-challenge"
    assert (ch_dir / "challenge.yaml").is_file()
    assert (ch_dir / "files" / "README.md").is_file()

    module_data = yaml.safe_load((sandbox_curriculum / "modules" / "99-test-admin" / "module.yaml").read_text())
    assert "test-admin-probe-challenge" in module_data["challenges"]

    engine.reload()
    assert "test-admin-probe-challenge" in engine._challenges


def test_save_and_list_proposals(sandbox_curriculum):
    from academy.admin import list_proposals, save_proposal

    result = save_proposal(
        sandbox_curriculum,
        kind="curriculum_note",
        title="Move module later",
        body={"module_slug": "test-admin"},
        notes="Consider a side-path dojo",
    )
    assert result["ok"] is True
    rows = list_proposals(sandbox_curriculum)
    assert len(rows) == 1
    assert rows[0]["kind"] == "curriculum_note"


def test_curriculum_overview(engine, monkeypatch):
    from academy.admin import curriculum_overview

    _unlock_admin(monkeypatch)
    overview = curriculum_overview(engine)
    assert overview["module_count"] == len(list(CURRICULUM.glob("modules/*/module.yaml")))
    assert overview["challenge_count"] == len(list(CURRICULUM.glob("modules/*/challenges/*/challenge.yaml")))
    assert overview["admin_enabled"] is True
    assert overview["dojos"]


def test_admin_mode_unlocks_every_belt(engine, monkeypatch):
    from academy.dojos import catalog_payload, dojo_stats

    monkeypatch.delenv("ACADEMY_ADMIN", raising=False)
    assert any(d.locked for d in dojo_stats(engine)), "a fresh learner has locked belts"
    assert catalog_payload(engine)["challenge_index"] == []

    monkeypatch.setenv("ACADEMY_ADMIN", "1")
    assert any(d.locked for d in dojo_stats(engine)), "ACADEMY_ADMIN=1 without the password unlocks nothing"
    _unlock_admin(monkeypatch)
    assert not any(d.locked for d in dojo_stats(engine))
    cat = catalog_payload(engine)
    assert cat["admin"] is True
    ids = {row["id"] for row in cat["challenge_index"]}
    assert {"zt-first-commands", "cppq-cmake", "pyq-generics"} <= ids
    engine.start_challenge("pyq-generics")
    assert (engine.workspace_root / "tasks.py").is_file()


def test_four_belts_white_to_blue(engine):
    from academy.dojos import load_dojos

    belts = [d.belt for d in load_dojos(engine.curriculum_root).core]
    assert belts == ["white", "yellow", "orange", "blue"]
    assert len(engine.challenges) == 110


def test_toggles_hide_dojos_and_challenges(engine):
    from academy.admin import curriculum_overview, set_toggle
    from academy.dojos import catalog_payload, dojo_detail, dojo_stats

    first, second = [d for d in dojo_stats(engine) if d.kind == "core"][:2]
    total = engine.status_summary()["total"]
    cid = dojo_detail(engine, first.id)["modules_detail"][0]["challenges"][0]["id"]

    assert set_toggle(engine, "challenge", cid, False)["ok"]
    assert cid not in {c["id"] for m in dojo_detail(engine, first.id)["modules_detail"] for c in m["challenges"]}
    assert engine.status_summary()["total"] == total - 1
    with pytest.raises(KeyError):
        engine.get_challenge(cid)
    with pytest.raises(KeyError):
        engine.start_challenge(cid)
    assert engine.get_challenge(cid, include_disabled=True).id == cid

    assert set_toggle(engine, "dojo", second.id, False)["ok"]
    ids = [d["id"] for d in catalog_payload(engine)["dojos"]]
    assert second.id not in ids and first.id in ids
    assert dojo_detail(engine, second.id) is None
    hidden = engine.module_challenges(second.module_slugs[0], include_disabled=True)[0].id
    with pytest.raises(KeyError):
        engine.get_challenge(hidden)

    # The admin overview still lists everything, with its switch state.
    ov = {d["id"]: d for d in curriculum_overview(engine)["dojos"]}
    assert ov[second.id]["enabled"] is False
    assert any(c["id"] == cid and c["enabled"] is False for m in ov[first.id]["modules"] for c in m["challenges"])

    # Switches persist on disk and switch back on.
    from academy.engine import AcademyEngine

    fresh = AcademyEngine(curriculum_root=engine.curriculum_root, data_dir=engine.data_dir, workspace_root=engine.workspace_root)
    assert not fresh.dojo_enabled(second.id) and not fresh.challenge_enabled(cid)
    set_toggle(fresh, "dojo", second.id, True)
    set_toggle(fresh, "challenge", cid, True)
    assert engine.dojo_enabled(second.id) and engine.challenge_enabled(cid)
    assert engine.status_summary()["total"] == total


def test_toggle_rejects_unknown_ids(engine):
    from academy.admin import set_toggle

    assert not set_toggle(engine, "dojo", "no-such-dojo", False)["ok"]
    assert not set_toggle(engine, "challenge", "no-such-challenge", False)["ok"]
    assert not set_toggle(engine, "belt", "x", False)["ok"]


def test_dojo_with_every_challenge_off_is_hidden_and_does_not_block(engine):
    from academy.admin import set_toggle
    from academy.dojos import dojo_stats

    first, second = [d for d in dojo_stats(engine) if d.kind == "core"][:2]
    assert second.locked
    for slug in first.module_slugs:
        for c in engine.module_challenges(slug):
            set_toggle(engine, "challenge", c.id, False)
    stats = {d.id: d for d in dojo_stats(engine)}
    assert first.id not in stats
    assert not stats[second.id].locked


def test_reader_serves_challenge_images(tmp_path):
    """Every ![...](media/x.png) in a README/LESSON resolves, and nothing outside files/media/ is served."""
    import re
    from types import SimpleNamespace

    from academy.dojos import challenge_docs, challenge_media

    png = b"\x89PNG\r\n\x1a\n" + b"\0" * 16
    (tmp_path / "files" / "media").mkdir(parents=True)
    (tmp_path / "files" / "media" / "map.png").write_bytes(png)
    (tmp_path / "files" / "README.md").write_text("# Task\n\n![map](media/map.png)\n", encoding="utf-8")
    c = SimpleNamespace(path=tmp_path / "challenge.yaml")
    names = {m for d in challenge_docs(c) for m in re.findall(r"!\[[^\]]*\]\(media/([^)]+)\)", d["text"])}
    assert names == {"map.png"}
    for name in names:
        data, ctype = challenge_media(c, name)
        assert ctype == "image/png" and data.startswith(b"\x89PNG")
    for bad in ("../README.md", "..", ".hidden.png", "missing.png", "README.md", "a/b.png"):
        assert challenge_media(c, bad) is None
