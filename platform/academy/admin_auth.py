"""Admin password: set once on first run, required every time admin mode is turned on.

The salted PBKDF2 hash lives in <data dir>/admin.json (offline, stdlib only).
Typing the password sets ACADEMY_ADMIN_UNLOCK in this process, so the server and
anything it runs see admin mode without asking again. ACADEMY_ADMIN=1 alone does nothing.

Forgot it? Delete <data dir>/admin.json (or run: ./academy admin --reset-password)
and the next run asks for a new one.
"""

from __future__ import annotations

import getpass
import hashlib
import json
import os
import sys
from pathlib import Path

from .classroom import MAX_PASSWORD, MIN_PASSWORD, hash_password, verify_password

UNLOCK_ENV = "ACADEMY_ADMIN_UNLOCK"
FILENAME = "admin.json"


def data_dir() -> Path:
    # Same default as cli._paths(); run.sh and ./academy set ACADEMY_DATA to <folder>/.academy-data.
    return Path(os.environ.get("ACADEMY_DATA", str(Path.home() / ".academy")))


def password_file(base: Path | None = None) -> Path:
    return (base or data_dir()) / FILENAME


def _load(base: Path | None = None) -> dict:
    try:
        data = json.loads(password_file(base).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _save(record: dict, base: Path | None = None) -> Path:
    path = password_file(base)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=2)
    os.replace(tmp, path)
    return path


def has_password(base: Path | None = None) -> bool:
    return bool(_load(base).get("hash"))


def setup_skipped(base: Path | None = None) -> bool:
    return bool(_load(base).get("skipped"))


def set_password(password: str, base: Path | None = None) -> Path:
    if not MIN_PASSWORD <= len(password) <= MAX_PASSWORD:
        raise ValueError(f"password must be at least {MIN_PASSWORD} characters")
    return _save(hash_password(password), base)


def check_password(password: str, base: Path | None = None) -> bool:
    record = _load(base)
    return bool(record.get("hash")) and verify_password(password, record)


def reset_password(base: Path | None = None) -> bool:
    try:
        password_file(base).unlink()
        return True
    except FileNotFoundError:
        return False


def _unlock_token(record: dict) -> str:
    return hashlib.sha256(f"academy-admin-unlock:{record.get('salt')}:{record.get('hash')}".encode()).hexdigest()


def unlock(base: Path | None = None) -> None:
    """Mark this process (and its children) as unlocked. Call only after check_password()."""
    os.environ[UNLOCK_ENV] = _unlock_token(_load(base))


def is_unlocked(base: Path | None = None) -> bool:
    record = _load(base)
    token = os.environ.get(UNLOCK_ENV, "")
    return bool(record.get("hash")) and bool(token) and token == _unlock_token(record)


# ── terminal prompts ───────────────────────────────────────────────────────


def _interactive() -> bool:
    return sys.stdin.isatty()


def prompt_new_password(*, allow_skip: bool = False, base: Path | None = None) -> bool:
    """Ask for a new admin password twice and save it. False if skipped or it failed."""
    skip = " (Enter to skip)" if allow_skip else ""
    for _ in range(3):
        pw = getpass.getpass(f"New admin password{skip}: ")
        if not pw and allow_skip:
            _save({"skipped": True}, base)
            print("  Skipped. You'll be asked again the first time you turn on admin mode.")
            return False
        if len(pw) < MIN_PASSWORD:
            print(f"  Must be at least {MIN_PASSWORD} characters.", file=sys.stderr)
            continue
        if getpass.getpass("Again: ") != pw:
            print("  Passwords differ.", file=sys.stderr)
            continue
        path = set_password(pw, base)
        print(f"  Admin password saved (salted hash in {path}).")
        return True
    return False


def first_run_setup(base: Path | None = None) -> None:
    """On the very first ./run.sh, offer to set the admin password. Never blocks a learner."""
    if has_password(base) or setup_skipped(base) or not _interactive():
        return
    print("  First run: set the admin password. Admin mode (every belt unlocked,")
    print("  curriculum editor) will ask for it.")
    prompt_new_password(allow_skip=True, base=base)
    print("")


def require_admin(base: Path | None = None) -> bool:
    """Gate for every way of turning admin mode on. True once the right password is typed."""
    if is_unlocked(base):
        return True
    if not _interactive():
        print("Admin mode needs the admin password; run it from a terminal.", file=sys.stderr)
        return False
    if not has_password(base):
        print("No admin password yet. Set one now; admin mode will ask for it from now on.")
        if not prompt_new_password(base=base):
            return False
        unlock(base)
        return True
    for _ in range(3):
        if check_password(getpass.getpass("Admin password: "), base):
            unlock(base)
            return True
        print("  Wrong password.", file=sys.stderr)
    print(f"Forgot it? Delete {password_file(base)} (or ./academy admin --reset-password) and set a new one.", file=sys.stderr)
    return False
