"""Classroom mode: many learners, one server (stdlib only).

academy serve --host <ip>  turns this on. It adds:
  * accounts   — username + password (salted PBKDF2), users file in the server data dir
  * sessions   — random token in an HttpOnly SameSite=Strict cookie; only sha256(token) is kept,
                 in memory and in sessions.json (0600), so a server restart keeps people logged in
  * isolation  — data/users/<name>/{challenge, .academy, flag.txt} per learner (folders 0700),
                 passed explicitly to a per-user engine (never via os.environ). Progress is
                 written to users/<name>/.academy/progress.json on every change (autosave).
  * sync       — progress/<name>.json committed + pushed to a shared git clone

SECURITY CAVEAT: all learner folders belong to the server's OS account. Learners can
read each other's folders (and the users file hashes). Run on a dedicated Pi/VM/container.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import secrets
import subprocess
import sys
import threading
import time
from collections import deque
from pathlib import Path
from types import SimpleNamespace

from .progress import ChallengeProgress, ProgressStore

USERNAME_RE = re.compile(r"^[a-z][a-z0-9_-]{2,31}$")
USERNAME_RULE = "3-32 characters: lowercase letters, digits, - or _, starting with a letter."
PBKDF2_ITERATIONS = 240_000
MIN_PASSWORD = 8
MAX_PASSWORD = 1024
SESSION_TTL = 12 * 3600  # sliding
COOKIE = "academy_session"
PRIVATE_DIR = 0o700  # data dir, users/ and every users/<name>/: only the server's OS account
_CID_RE = re.compile(r"^[A-Za-z0-9._-]{1,100}$")


def log(msg: str) -> None:
    # Never pass passwords, tokens or flags in here.
    print(time.strftime("%Y-%m-%d %H:%M:%S"), "[classroom]", msg, file=sys.stderr, flush=True)


# ── passwords ──────────────────────────────────────────────────────────────


def hash_password(password: str, *, salt: bytes | None = None, iterations: int = PBKDF2_ITERATIONS) -> dict:
    salt = salt if salt is not None else secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return {"alg": "pbkdf2_sha256", "iterations": iterations, "salt": salt.hex(), "hash": digest.hex()}


def verify_password(password: str, record: dict) -> bool:
    try:
        salt = bytes.fromhex(record["salt"])
        iterations = int(record["iterations"])
        expected = bytes.fromhex(record["hash"])
    except (KeyError, TypeError, ValueError):
        return False
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return hmac.compare_digest(digest, expected)


_DUMMY = hash_password("timing-equalizer")


def valid_username(name: object) -> bool:
    return isinstance(name, str) and bool(USERNAME_RE.fullmatch(name))


def private_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(path, PRIVATE_DIR)
    except OSError:
        pass  # e.g. a mounted folder that ignores modes
    return path


def _write_private(path: Path, data) -> None:
    """Atomic write of a 0600 JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f".{os.getpid()}.{threading.get_ident()}.tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, sort_keys=True)
        fh.write("\n")
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


class UserStore:
    """data/users.json: {name: {alg, iterations, salt, hash, created}}. Never in git."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self._lock = threading.Lock()

    def _load(self) -> dict:
        if not self.path.is_file():
            return {}
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}

    def _save(self, data: dict) -> None:
        _write_private(self.path, data)

    def get(self, name: str) -> dict | None:
        with self._lock:
            rec = self._load().get(name)
        return rec if isinstance(rec, dict) else None

    def create(self, name: str, password: str) -> bool:
        """Add a user; False if the name is taken."""
        if not valid_username(name):
            raise ValueError(USERNAME_RULE)
        record = hash_password(password)  # slow part outside the lock
        with self._lock:
            data = self._load()
            if name in data:
                return False
            record["created"] = int(time.time())
            data[name] = record
            self._save(data)
        return True

    def set_password(self, name: str, password: str) -> bool:
        """Change an existing user's password; False if no such user."""
        record = hash_password(password)
        with self._lock:
            data = self._load()
            if name not in data:
                return False
            record["created"] = data[name].get("created", int(time.time()))
            data[name] = record
            self._save(data)
        return True


class Sessions:
    """Sessions keyed by sha256(token). With a path they survive a server restart (sessions.json, 0600).

    The file holds hashes only, so reading it does not let anyone log in. Sliding expiry is
    written back at most every PERSIST_EVERY seconds, not on every request.
    """

    PERSIST_EVERY = 600.0

    def __init__(self, ttl: float = SESSION_TTL, path: Path | None = None):
        self.ttl = ttl
        self.path = Path(path) if path else None
        self._lock = threading.Lock()
        self._by_hash: dict[str, list] = {}  # hash -> [user, expires]
        self._saved_at = 0.0
        if self.path and self.path.is_file():
            try:
                raw = json.loads(self.path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                raw = {}
            now = time.time()
            for key, entry in (raw.items() if isinstance(raw, dict) else ()):
                if (isinstance(entry, list) and len(entry) == 2 and valid_username(entry[0])
                        and isinstance(entry[1], (int, float)) and entry[1] > now):
                    self._by_hash[key] = [entry[0], float(entry[1])]

    def _persist(self) -> None:
        """Call with the lock held."""
        if not self.path:
            return
        now = time.time()
        live = {k: v for k, v in self._by_hash.items() if v[1] > now}
        self._by_hash = live
        try:
            _write_private(self.path, live)
            self._saved_at = now
        except OSError as exc:
            log(f"could not save sessions: {exc}")

    @staticmethod
    def _key(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def create(self, user: str) -> str:
        token = secrets.token_urlsafe(32)
        with self._lock:
            self._by_hash[self._key(token)] = [user, time.time() + self.ttl]
            self._persist()
        return token

    def user_for(self, token: str | None) -> str | None:
        if not token or len(token) > 200:
            return None
        key = self._key(token)
        now = time.time()
        with self._lock:
            # Looking up the sha256 of the token (not the token) keeps timing useless to an attacker.
            entry = self._by_hash.get(key)
            if not entry:
                return None
            if entry[1] < now:
                del self._by_hash[key]
                return None
            entry[1] = now + self.ttl
            if self.path and now - self._saved_at > self.PERSIST_EVERY:
                self._persist()
            return entry[0]

    def drop(self, token: str | None) -> str | None:
        if not token:
            return None
        with self._lock:
            entry = self._by_hash.pop(self._key(token), None)
            if entry:
                self._persist()
        return entry[0] if entry else None


class RateLimiter:
    """Sliding-window counters, e.g. failed logins per IP and per username."""

    def __init__(self, window: float = 300.0):
        self.window = window
        self._lock = threading.Lock()
        self._hits: dict[str, deque] = {}

    def _prune(self, key: str, now: float) -> deque:
        q = self._hits.setdefault(key, deque())
        while q and q[0] < now - self.window:
            q.popleft()
        return q

    def allowed(self, key: str, limit: int) -> bool:
        now = time.time()
        with self._lock:
            ok = len(self._prune(key, now)) < limit
            if len(self._hits) > 10_000:  # bound memory
                for k in [k for k, q in self._hits.items() if not q]:
                    del self._hits[k]
            return ok

    def hit(self, key: str) -> None:
        with self._lock:
            self._prune(key, time.time()).append(time.time())


# ── progress export / restore ──────────────────────────────────────────────


def export_progress(username: str, store: ProgressStore) -> dict:
    """What goes into the shared repo: timestamps + counters only. No flags, paths, secrets."""
    challenges = {}
    for cid, p in sorted(store.challenges.items()):
        challenges[cid] = {
            "solved": bool(p.solved),
            "started_at": p.started_at,
            "completed_at": p.completed_at,
            "hints_revealed": int(p.hints_revealed),
            "attempts": int(p.attempts),
        }
    return {
        "user": username,
        "solved": sum(1 for c in challenges.values() if c["solved"]),
        "challenges": challenges,
    }


def _num(v) -> float | None:
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) and v >= 0 else None


def _count(v) -> int:
    return int(v) if isinstance(v, int) and not isinstance(v, bool) and 0 <= v < 1_000_000 else 0


def store_from_export(data: object, username: str) -> ProgressStore | None:
    """Validate a repo progress file (it is untrusted text) and rebuild a ProgressStore."""
    if not isinstance(data, dict) or data.get("user") != username:
        return None
    raw = data.get("challenges")
    if not isinstance(raw, dict):
        return None
    store = ProgressStore(student_id=username)
    for cid, c in raw.items():
        if not isinstance(cid, str) or not _CID_RE.fullmatch(cid) or not isinstance(c, dict):
            continue
        store.challenges[cid] = ChallengeProgress(
            started_at=_num(c.get("started_at")),
            completed_at=_num(c.get("completed_at")),
            hints_revealed=_count(c.get("hints_revealed")),
            attempts=_count(c.get("attempts")),
            solved=c.get("solved") is True,
        )
    return store


class ProgressSync:
    """Commit progress/<user>.json into a local git clone; pull --rebase + push in the background.

    The admin sets up the remote and credentials. Local progress.json stays the source of
    truth, so a failed push only delays sharing — nothing is lost; we retry later.
    """

    def __init__(self, repo: Path, *, debounce: float = 5.0, retry: float = 60.0, start: bool = True):
        self.repo = Path(repo).resolve()
        r = self._git("rev-parse", "--is-inside-work-tree", check=False)
        if r.returncode != 0 or r.stdout.strip() != "true":
            raise ValueError(f"--progress-repo {self.repo} is not a git clone")
        self.debounce = debounce
        self.retry = retry
        self.lock = threading.Lock()  # serializes all git/worktree access
        self.cv = threading.Condition()
        self.pending: dict[str, dict] = {}
        self.need_push = True  # push anything a previous run left committed but unpushed
        self.last_error = ""
        if start:
            threading.Thread(target=self._loop, name="progress-sync", daemon=True).start()

    def _git(self, *args: str, check: bool = True, author: str | None = None) -> subprocess.CompletedProcess:
        env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_ASKPASS="true")
        cmd = ["git", "-C", str(self.repo)]
        if author:
            cmd += ["-c", f"user.name={author}", "-c", f"user.email={author}@academy.local"]
        r = subprocess.run(cmd + list(args), env=env, capture_output=True, text=True, timeout=180, check=False)
        if check and r.returncode != 0:
            raise RuntimeError(f"git {args[0]} failed: {(r.stderr or r.stdout).strip()[-300:]}")
        return r

    def path_for(self, user: str) -> Path:
        assert valid_username(user)
        return self.repo / "progress" / f"{user}.json"

    def schedule(self, user: str, store: ProgressStore) -> None:
        snapshot = export_progress(user, store)
        with self.cv:
            self.pending[user] = snapshot
            self.cv.notify()

    def read(self, user: str) -> dict | None:
        with self.lock:
            p = self.path_for(user)
            if not p.is_file():
                return None
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                return None

    def _loop(self) -> None:
        while True:
            with self.cv:
                while not self.pending and not self.need_push:
                    self.cv.wait()
            time.sleep(self.debounce)  # debounce: fold a burst of saves into one push
            with self.cv:
                batch, self.pending = self.pending, {}
            try:
                ok = self.flush(batch)
            except Exception as exc:  # noqa: BLE001 — keep the thread alive
                log(f"progress sync crashed: {exc}")
                ok = False
            if not ok:
                time.sleep(self.retry)

    def flush(self, batch: dict[str, dict]) -> bool:
        with self.lock:
            for user, data in batch.items():
                try:
                    path = self.path_for(user)
                    path.parent.mkdir(parents=True, exist_ok=True)
                    tmp = path.with_suffix(".json.tmp")
                    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
                    tmp.replace(path)
                    rel = str(path.relative_to(self.repo))
                    self._git("add", "--", rel)
                    if self._git("diff", "--cached", "--quiet", "--", rel, check=False).returncode == 1:
                        msg = f"{user}: {data.get('solved', 0)} solved"
                        self._git("commit", "-q", "-m", msg, "--", rel, author=user)
                        self.need_push = True
                except Exception as exc:  # noqa: BLE001
                    log(f"progress commit for {user} failed (will retry): {exc}")
                    with self.cv:
                        self.pending.setdefault(user, data)  # keep a newer snapshot if one arrived
                    return False
            if not self.need_push or self._git("rev-parse", "-q", "--verify", "HEAD", check=False).returncode:
                self.need_push = False  # nothing committed yet (fresh empty clone): nothing to push
                return True
            # A brand-new empty shared repo has no branch to pull yet; the first push creates it.
            if self._git("ls-remote", "--heads", "origin", check=False).stdout.strip():
                pull = self._git("pull", "--rebase", "--autostash", "-q", "origin", "HEAD", check=False)
                if pull.returncode != 0:
                    self._git("rebase", "--abort", check=False)
                    return self._fail("pull", pull)
            push = self._git("push", "-q", "-u", "origin", "HEAD", check=False)
            if push.returncode != 0:
                return self._fail("push", push)
            self.need_push = False
            if self.last_error:
                log("progress sync recovered; pushed")
            self.last_error = ""
            return True

    def _fail(self, what: str, r: subprocess.CompletedProcess) -> bool:
        # ponytail: offline labs just keep retrying every `retry` seconds; commits stay local meanwhile.
        err = f"git {what} failed (will retry): {(r.stderr or r.stdout).strip()[-300:]}"
        if err != self.last_error:
            log(err)
        self.last_error = err
        return False


# ── the classroom ──────────────────────────────────────────────────────────


def workspace_shortcut(name: str, ws: Path) -> str | None:
    """~/dojo/<name> -> users/<name>/challenge, so a learner at this machine (a laptop, WSL)
    can `cd ~/dojo/<name>` instead of typing the long folder under .academy-data.

    Best effort: never replaces a real file or folder, and returns None when it cannot make the link.
    """
    if os.environ.get("ACADEMY_WORKSPACE_LINKS", "1").strip().lower() in {"0", "false", "no", "off"}:
        return None
    try:
        link = Path.home() / "dojo" / name
        if link.is_symlink():
            if Path(os.readlink(link)) == ws:
                return f"~/dojo/{name}"
            link.unlink()
        elif link.exists():
            return None
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(ws, target_is_directory=True)
        return f"~/dojo/{name}"
    except (OSError, RuntimeError):
        return None


class Classroom:
    def __init__(self, base_engine, data_dir: Path, *, signup: bool = True, sync: ProgressSync | None = None):
        self.base = base_engine
        self.data_dir = Path(data_dir).resolve()
        self.users_dir = self.data_dir / "users"
        private_dir(self.data_dir)
        private_dir(self.users_dir)
        self.users = UserStore(self.data_dir / "users.json")
        self.sessions = Sessions(path=self.data_dir / "sessions.json")
        self.limiter = RateLimiter()
        self.signup = signup
        self.sync = sync
        self._lock = threading.Lock()
        self._ctx: dict[str, SimpleNamespace] = {}
        self._making: dict[str, threading.Lock] = {}

    # per-user paths: everything explicit, nothing through os.environ
    def user_root(self, name: str) -> Path:
        if not valid_username(name):
            raise ValueError("bad username")
        return self.users_dir / name

    def ctx(self, name: str) -> SimpleNamespace:
        with self._lock:
            c = self._ctx.get(name)
        if c:
            return c
        with self._lock:
            make = self._making.setdefault(name, threading.Lock())
        with make:  # one builder per user; others wait here, not on the global lock
            with self._lock:
                c = self._ctx.get(name)
            if c:
                return c
            c = self._build_ctx(name)
            with self._lock:
                self._ctx[name] = c
            return c

    def _build_ctx(self, name: str) -> SimpleNamespace:
        root = self.user_root(name)
        data, ws, flag = root / ".academy", root / "challenge", root / "flag.txt"
        private_dir(root)
        for d in (data, ws):
            d.mkdir(parents=True, exist_ok=True)
        rc = root / ".bashrc"
        if not rc.exists():
            rc.write_text(
                f"PS1='{name}@academy:\\w\\$ '\nalias ll='ls -la'\n"
                "echo 'You are in your challenge folder. Try: ls   then: cat README*'\n",
                encoding="utf-8",
            )
        eng = self.base.for_user(data, ws, flag)
        eng.workspace_link = workspace_shortcut(name, ws)
        if self.sync:
            if not eng.progress_repo.path.exists():
                restored = store_from_export(self.sync.read(name), name)
                if restored and restored.challenges:
                    eng.progress_repo.save(restored)
                    log(f"restored {name}'s progress from the shared repo")
            eng.progress_repo.on_save = lambda store, n=name: self.sync.schedule(n, store)
        return SimpleNamespace(name=name, engine=eng, lock=threading.RLock(), root=root, workspace=ws, flag=flag)

    def login(self, username: object, password: object, ip: str, *, create: bool = False) -> tuple[int, dict, str | None]:
        """Log in to an existing account, or (create=True) make a new one and log in to it.

        Two explicit steps, so a typo in a username never silently starts a fresh, empty account.
        """
        name = username.strip().lower() if isinstance(username, str) else ""
        if not self.limiter.allowed(f"ip:{ip}", 20) or not self.limiter.allowed(f"user:{name}", 8):
            return 429, {"error": "Too many attempts. Wait a few minutes and try again."}, None
        if not valid_username(name):
            return 400, {"error": "Username must be " + USERNAME_RULE}, None
        if not isinstance(password, str) or not password or len(password) > MAX_PASSWORD:
            return 400, {"error": "Enter a password."}, None
        if create:
            if not self.signup:
                return 403, {"error": "New accounts are made by your instructor. Ask them for a username."}, None
            if len(password) < MIN_PASSWORD:
                return 400, {"error": f"Pick a password of at least {MIN_PASSWORD} characters."}, None
            if not self.limiter.allowed(f"signup:{ip}", 40):
                return 429, {"error": "Too many new accounts from here. Wait a few minutes."}, None
            self.limiter.hit(f"signup:{ip}")
            if not self.users.create(name, password):
                return 409, {"error": f"The username {name} is taken. Log in instead, or pick another name."}, None
            log(f"new account {name} from {ip}")
        else:
            rec = self.users.get(name)
            if not verify_password(password, rec if rec else _DUMMY) or rec is None:
                self.limiter.hit(f"ip:{ip}")
                self.limiter.hit(f"user:{name}")
                log(f"failed login for {name!r} from {ip}")
                return 401, {"error": "Wrong username or password. New here? Choose Create account."}, None
        self.ctx(name)  # create the private folder + restore progress before the first page load
        token = self.sessions.create(name)
        return 200, {"ok": True, "user": name, "created": bool(create)}, token

    def logout(self, token: str | None) -> None:
        self.sessions.drop(token)
