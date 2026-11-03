"""Save and restore a learner's progress and challenge files as one .zip. Offline-only.

Starting a challenge wipes the challenge folder, so before that happens the files the
learner wrote or changed are kept in data_dir/work/<challenge-id>/ and put back the next
time that challenge starts. A save file is a plain zip anyone can open:

    the-dojo-save.json   what this is, when it was made, whose it is
    progress.json           solved challenges, hints, attempts
    work/<challenge-id>/…   the learner's own files for each challenge

Restoring merges: nothing already solved or kept on this machine is lost.
"""

from __future__ import annotations

import hashlib
import io
import json
import re
import shutil
import stat
import time
import zipfile
from pathlib import Path, PurePosixPath
from typing import BinaryIO

from .progress import ChallengeProgress, ProgressRepository, ProgressStore

FORMAT = "the-dojo-save"
VERSION = 1
MANIFEST = "the-dojo-save.json"
EARLIER_SAVES = {"signal-dojo-save.json": "signal-dojo-save"}  # manifest -> format, from before the rename
WORK = "work"
STAGED = "staged.json"  # hashes of the challenge folder right after Start: anything else is the learner's

MAX_FILE = 5 << 20  # skip bigger files (captures, recordings): they come back with the challenge
MAX_PER_CHALLENGE = 50 << 20
MAX_UNPACKED = 512 << 20
SKIP_NAMES = {".challenge", ".flagpath", ".lab_env", "__pycache__", ".academy_write_probe", ".git"}
SKIP_SUFFIXES = {".pyc", ".o"}
_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$")


class SaveFileError(ValueError):
    """The file is not a save from The Dojo, or is damaged."""


def _sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def _files(root: Path):
    """(posix relative path, path) for every regular file worth keeping under root."""
    if not root.is_dir():
        return
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(part in SKIP_NAMES for part in rel.parts) or path.suffix in SKIP_SUFFIXES:
            continue
        if path.is_symlink() or not path.is_file():
            continue
        yield rel.as_posix(), path


def _hashes(root: Path) -> dict[str, str]:
    out = {}
    for rel, path in _files(root):
        try:
            out[rel] = _sha(path)
        except OSError:  # unreadable starter file (permission puzzles): never the learner's
            out[rel] = ""
    return out


def record_staged(data_dir: Path, workspace: Path, challenge_id: str) -> None:
    """Remember what Start put in the folder, so only the learner's own files get kept."""
    path = Path(data_dir) / STAGED
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"challenge_id": challenge_id, "files": _hashes(workspace)}), encoding="utf-8")


def _staged(data_dir: Path, challenge_id: str) -> dict[str, str] | None:
    try:
        data = json.loads((Path(data_dir) / STAGED).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if data.get("challenge_id") != challenge_id or not isinstance(data.get("files"), dict):
        return None
    return data["files"]


def keep_work(data_dir: Path, workspace: Path, starter_dir: Path | None = None) -> tuple[str | None, int]:
    """Copy the learner's new or changed files out of the challenge folder.

    Returns (challenge id, files kept). Earlier kept files stay when nothing new was written.
    """
    marker = Path(workspace) / ".challenge"
    try:
        cid = marker.read_text(encoding="utf-8").strip()
    except OSError:
        return None, 0
    if not _SAFE_ID.match(cid):
        return None, 0
    baseline = _staged(data_dir, cid)
    if baseline is None:  # folder staged before this feature existed: compare with the starter files
        baseline = _hashes(starter_dir) if starter_dir else {}
    mine: list[tuple[str, Path]] = []
    total = 0
    for rel, path in _files(Path(workspace)):
        try:
            size = path.stat().st_size
            if size > MAX_FILE or total + size > MAX_PER_CHALLENGE:
                continue
            if baseline.get(rel) == _sha(path):
                continue
        except OSError:
            continue
        mine.append((rel, path))
        total += size
    if not mine:
        return cid, 0
    dest = Path(data_dir) / WORK / cid
    tmp = dest.with_name(f".{cid}.tmp")
    shutil.rmtree(tmp, ignore_errors=True)
    for rel, path in mine:
        target = tmp / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        target.chmod(stat.S_IMODE(path.stat().st_mode) | 0o600)
    shutil.rmtree(dest, ignore_errors=True)
    tmp.rename(dest)
    return cid, len(mine)


def restore_work(data_dir: Path, workspace: Path, challenge_id: str, skip: set[str] = frozenset()) -> int:
    """Put kept files back into a freshly started challenge folder."""
    src = Path(data_dir) / WORK / challenge_id
    count = 0
    for rel, path in _files(src):
        if rel in skip:
            continue
        target = Path(workspace) / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and not target.is_file():
            continue
        if target.exists():
            target.chmod(stat.S_IMODE(target.stat().st_mode) | 0o600)
        shutil.copyfile(path, target)
        target.chmod(stat.S_IMODE(path.stat().st_mode))
        count += 1
    return count


def kept_challenges(data_dir: Path) -> list[str]:
    root = Path(data_dir) / WORK
    if not root.is_dir():
        return []
    return sorted(p.name for p in root.iterdir() if p.is_dir() and _SAFE_ID.match(p.name) and any(p.rglob("*")))


def export_zip(data_dir: Path, out: BinaryIO, *, name: str = "") -> dict:
    """Write the save file to `out`. Returns a short summary."""
    data_dir = Path(data_dir)
    progress = data_dir / "progress.json"
    store = ProgressRepository(progress).load() if progress.is_file() else ProgressStore()
    kept = kept_challenges(data_dir)
    summary = {
        "format": FORMAT,
        "version": VERSION,
        "saved_at": time.time(),
        "name": str(name or "")[:32],
        "solved": sum(1 for c in store.challenges.values() if c.solved),
        "challenges_with_files": len(kept),
    }
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(MANIFEST, json.dumps(summary, indent=2) + "\n")
        zf.writestr("progress.json", json.dumps(store.to_dict(), indent=2, sort_keys=True) + "\n")
        if (data_dir / "feedback.jsonl").is_file():  # so a learner can send their feedback with their save
            zf.write(data_dir / "feedback.jsonl", "feedback.jsonl")
        for cid in kept:
            for rel, path in _files(data_dir / WORK / cid):
                info = zipfile.ZipInfo(f"{WORK}/{cid}/{rel}", time.localtime(path.stat().st_mtime)[:6])
                info.external_attr = (stat.S_IFREG | stat.S_IMODE(path.stat().st_mode)) << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                zf.writestr(info, path.read_bytes())
    return summary


def merge_progress(local: ProgressStore, incoming: ProgressStore) -> ProgressStore:
    """Union of both: solved anywhere stays solved; earliest dates, highest counts win."""

    def first(a, b):
        return min(x for x in (a, b) if x is not None) if a is not None or b is not None else None

    for cid, theirs in incoming.challenges.items():
        mine = local.challenges.get(cid)
        if mine is None:
            local.challenges[cid] = theirs
            continue
        local.challenges[cid] = ChallengeProgress(
            started_at=first(mine.started_at, theirs.started_at),
            completed_at=first(mine.completed_at, theirs.completed_at) if (mine.solved or theirs.solved) else None,
            hints_revealed=max(mine.hints_revealed, theirs.hints_revealed),
            attempts=max(mine.attempts, theirs.attempts),
            solved=mine.solved or theirs.solved,
            notes=mine.notes or theirs.notes,
        )
    for topic, items in incoming.mastered_topics.items():
        merged = list(local.mastered_topics.get(topic, []))
        merged += [i for i in items if i not in merged]
        local.mastered_topics[topic] = merged
    return local


def _read_store(raw: bytes) -> ProgressStore:
    try:
        data = json.loads(raw.decode("utf-8"))
        store = ProgressStore.from_dict(data)
    except (ValueError, TypeError, AttributeError) as exc:
        raise SaveFileError("The progress inside this save file is damaged.") from exc
    for cid, prog in store.challenges.items():
        if not isinstance(cid, str) or not isinstance(prog.solved, bool):
            raise SaveFileError("The progress inside this save file is damaged.")
    return store


def import_zip(data_dir: Path, src: BinaryIO | bytes, repo: ProgressRepository) -> dict:
    """Merge a save file into this machine's progress and kept files. Returns a summary."""
    if isinstance(src, (bytes, bytearray)):
        src = io.BytesIO(src)
    try:
        zf = zipfile.ZipFile(src)
    except (zipfile.BadZipFile, OSError) as exc:
        raise SaveFileError("That is not a save file from The Dojo (expected a .zip made by Save).") from exc
    with zf:
        names = set(zf.namelist())
        name, fmt = next(((m, f) for m, f in [(MANIFEST, FORMAT), *EARLIER_SAVES.items()] if m in names), (MANIFEST, FORMAT))
        try:
            manifest = json.loads(zf.read(name).decode("utf-8"))
        except (KeyError, ValueError) as exc:
            raise SaveFileError("That is not a save file from The Dojo (expected a .zip made by Save).") from exc
        if not isinstance(manifest, dict) or manifest.get("format") != fmt:
            raise SaveFileError("That is not a save file from The Dojo (expected a .zip made by Save).")
        if int(manifest.get("version", 0)) > VERSION:
            raise SaveFileError("This save file comes from a newer version of The Dojo. Update this copy first.")

        files: list[tuple[zipfile.ZipInfo, str, str]] = []
        total = 0
        for info in zf.infolist():
            if info.is_dir() or not info.filename.startswith(WORK + "/"):
                continue
            parts = PurePosixPath(info.filename).parts
            if len(parts) < 3 or not _SAFE_ID.match(parts[1]) or info.filename.startswith("/") or "\\" in info.filename:
                raise SaveFileError(f"Unsafe path in save file: {info.filename}")
            if any(p in ("", ".", "..") or p in SKIP_NAMES for p in parts[2:]):
                raise SaveFileError(f"Unsafe path in save file: {info.filename}")
            total += info.file_size
            if info.file_size > MAX_FILE or total > MAX_UNPACKED:
                raise SaveFileError("This save file is too large to restore.")
            files.append((info, parts[1], "/".join(parts[2:])))

        store = repo.load()
        if "progress.json" in zf.namelist():
            incoming = _read_store(zf.read("progress.json"))
            before = sum(1 for c in store.challenges.values() if c.solved)
            store = merge_progress(store, incoming)
            gained = sum(1 for c in store.challenges.values() if c.solved) - before
        else:
            gained = 0

        work = Path(data_dir) / WORK
        restored: set[str] = set()
        for info, cid, rel in files:
            target = work / cid / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(zf.read(info))
            mode = (info.external_attr >> 16) & 0o777
            target.chmod((mode or 0o644) | 0o600)
            restored.add(cid)
        repo.save(store)
    return {
        "ok": True,
        "name": str(manifest.get("name") or "")[:32],
        "saved_at": manifest.get("saved_at"),
        "solved": sum(1 for c in store.challenges.values() if c.solved),
        "newly_solved": gained,
        "challenges_with_files": len(restored),
    }


def default_filename(when: float | None = None) -> str:
    return time.strftime("the-dojo-save-%Y-%m-%d.zip", time.localtime(when))
