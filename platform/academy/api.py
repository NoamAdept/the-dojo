"""Local challenge API + dojo web UI (stdlib http.server). Offline-only."""

from __future__ import annotations

import errno
import gzip
import hashlib
import io
import ipaddress
import json
import os
import socket
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from .admin import (
    admin_enabled,
    apply_proposal,
    build_challenge_yaml,
    create_challenge,
    curriculum_overview,
    default_challenge_draft,
    list_proposals,
    module_detail,
    save_proposal,
    set_toggle,
    validate_challenge_draft,
)
from .backup import SaveFileError, default_filename
from .dojos import catalog_payload, challenge_docs, challenge_media, dojo_detail
from .engine import AcademyEngine
from .grading import award_flag
from .terminal_launch import open_workspace_terminal
from .ui_flavor import challenge_thumb_svg, display_title

STATIC_DIR = Path(__file__).resolve().parent / "static"
DOJO_HTML = STATIC_DIR / "dojo.html"
MAX_BODY = 1 << 20
MAX_SAVE_FILE = 64 << 20  # Restore uploads a whole save file
ADMIN_HTML = STATIC_DIR / "admin.html"
# Light on the Pi and on the lab network: compress text, let browsers keep fonts/icons, and answer
# a page reload with "304 Not Modified" instead of sending the 100+ KB page again.
GZIP_MIN = 1024
COMPRESSIBLE = ("text/", "application/json", "image/svg+xml")
STATIC_CACHE = "public, max-age=604800"  # fonts and belt icons: a week
CHECK_SLOTS = threading.BoundedSemaphore(2)  # ./check runs at once (each can load numpy); others wait their turn
_static_files: dict[Path, tuple] = {}
_static_lock = threading.Lock()


def _static(path: Path) -> tuple[bytes, bytes | None, str] | None:
    """(raw, gzipped or None, etag) for a file under static/, cached in memory until it changes on disk."""
    try:
        mtime = path.stat().st_mtime_ns
    except OSError:
        return None
    with _static_lock:
        hit = _static_files.get(path)
    if hit and hit[0] == mtime:
        return hit[1]
    raw = path.read_bytes()
    gz = gzip.compress(raw, 6, mtime=0) if len(raw) >= GZIP_MIN and path.suffix in (".html", ".svg", ".txt") else None
    entry = (raw, gz, '"' + hashlib.sha256(raw).hexdigest()[:20] + '"')
    with _static_lock:
        _static_files[path] = (mtime, entry)
    return entry
def _find_check(ws: Path) -> Path | None:
    for name in ("checker.py", "check.py"):
        candidate = ws / name
        if candidate.exists():
            return candidate
    check = ws / "check"
    if check.exists():
        return check
    return None


def _run_workspace_check(engine: AcademyEngine, challenge_id: str) -> dict:
    """Run the staged challenge checker; award + mark solved on success."""
    store = engine.progress()
    # Per-engine paths (explicit per user in classroom mode; never os.environ).
    ws = Path(store.current_workspace or engine.workspace_root)
    current = store.current_challenge_id
    marker = ws / ".challenge"
    marker_id = marker.read_text(encoding="utf-8").strip() if marker.is_file() else ""
    if current != challenge_id and marker_id != challenge_id:
        return {
            "ok": False,
            "error": "Start this challenge first (workspace does not match).",
            "workspace": str(ws),
        }
    check = _find_check(ws)
    if check is None:
        return {
            "ok": False,
            "error": "No checker in workspace. Paste a found flag instead.",
            "workspace": str(ws),
        }
    env = os.environ.copy()
    env["ACADEMY_WORKSPACE"] = str(ws)
    env["ACADEMY_DATA"] = str(engine.data_dir)
    env["ACADEMY_FLAG_PATH"] = str(engine.flag_path)
    env["PYTHONPATH"] = str(Path(__file__).resolve().parent.parent) + (
        os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else ""
    )
    if check.suffix == ".py":
        cmd = [sys.executable, str(check)]
    elif os.access(check, os.X_OK):
        cmd = [str(check)]
    else:
        cmd = ["bash", str(check)]
    with CHECK_SLOTS:
        result = subprocess.run(cmd, cwd=str(ws), env=env, check=False, capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        detail = (result.stdout or result.stderr or "").strip()
        return {
            "ok": False,
            "error": "Not done yet. This is what ./check says:",
            "detail": detail if len(detail) <= 800 else detail[-800:].partition("\n")[2],
            "workspace": str(ws),
        }
    flag = award_flag(ws, silent=True, data_dir_path=engine.data_dir, flag_path=engine.flag_path)
    submitted = engine.submit(challenge_id, flag)
    payload = {
        "ok": bool(submitted),
        "flag": flag if submitted else None,
        "workspace": str(ws),
        "via": "check",
    }
    if submitted:
        ch = engine.get_challenge(challenge_id)
        payload["explanation"] = ch.explanation
    return payload


def port_in_use_message(port: int) -> str:
    return (f"Port {port} is already in use: another Signal Dojo (often an older copy) is still running there,\n"
            f"and the browser would show that one. Stop it first (Ctrl-C in its window), or start this one\n"
            f"on another port: PORT={port + 1} ./run.sh")


def check_port(host: str, port: int) -> None:
    """Exit with a plain message when something already listens on host:port."""
    s = socket.socket()
    try:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # as the server does
        s.bind((host, port))
    except OSError as e:
        if e.errno == errno.EADDRINUSE:
            raise SystemExit(port_in_use_message(port)) from None
        # Any other problem (bad host, no permission) is the server's to report.
    finally:
        s.close()


def serve_api(
    curriculum_root: Path,
    data_dir: Path,
    host: str = "127.0.0.1",
    port: int = 8080,
    *,
    admin: bool = False,
    classroom=None,
    base_engine: AcademyEngine | None = None,
) -> None:
    """Single-user local console, or classroom mode when `classroom` is a classroom.Classroom."""
    engine = base_engine or AcademyEngine(curriculum_root=curriculum_root, data_dir=data_dir)
    if admin and classroom is None:
        os.environ["ACADEMY_ADMIN"] = "1"
    if classroom is not None:
        os.environ.pop("ACADEMY_ADMIN", None)  # learners never get admin unlocks
    cors = "*" if classroom is None else None  # classroom: same-origin only (cookies)

    def _admin_on() -> bool:
        return classroom is None and admin_enabled()  # never let learners edit curriculum

    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"  # keep-alive: one connection per browser tab, not one per request
        timeout = 30  # drop idle keep-alive connections so their threads end
        disable_nagle_algorithm = True  # headers and body go out as two writes; don't wait 40 ms between them

        def _admin_required(self):
            if _admin_on():
                return None
            return self._json(403, {"error": "Admin mode is off. Start it with ACADEMY_ADMIN=1 ./run.sh and type the admin password."})

        def _read_body(self) -> dict:
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                length = 0
            if length < 0 or length > MAX_BODY:
                raise ValueError("request body too large")
            raw = self.rfile.read(length) if length else b"{}"
            self._unread = 0
            try:
                body = json.loads(raw.decode("utf-8") or "{}")
            except json.JSONDecodeError:
                body = {}
            return body if isinstance(body, dict) else {}
        def _common_headers(self) -> None:
            if cors:
                self.send_header("Access-Control-Allow-Origin", cors)
            if classroom is not None:
                self.send_header("X-Content-Type-Options", "nosniff")
                self.send_header("X-Frame-Options", "DENY")
                self.send_header("Referrer-Policy", "no-referrer")

        def _gzip_ok(self) -> bool:
            return "gzip" in self.headers.get("Accept-Encoding", "")

        def _json(self, code: int, payload, cookie: str | None = None) -> None:
            data = json.dumps(payload, separators=(",", ":")).encode("utf-8")
            extra = []
            if cors:
                extra += [("Access-Control-Allow-Methods", "GET, POST, OPTIONS"), ("Access-Control-Allow-Headers", "Content-Type")]
            if cookie is not None:
                extra.append(("Set-Cookie", cookie))
            self._bytes(code, data, "application/json; charset=utf-8", extra=extra)

        def _bytes(self, code: int, data: bytes, content_type: str, *, cache: str = "no-store",
                   gz: bytes | None = None, etag: str | None = None, extra=()) -> None:
            if etag and self.headers.get("If-None-Match") == etag:
                self.send_response(304)
                self.send_header("ETag", etag)
                self.send_header("Cache-Control", cache)
                self._common_headers()
                self.end_headers()
                return
            compressible = content_type.startswith(COMPRESSIBLE)
            if compressible and self._gzip_ok():
                if gz is None and len(data) >= GZIP_MIN:
                    gz = gzip.compress(data, 5)
                if gz is not None:
                    data = gz
            else:
                gz = None
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            if gz is not None:
                self.send_header("Content-Encoding", "gzip")
            if compressible:
                self.send_header("Vary", "Accept-Encoding")
            if etag:
                self.send_header("ETag", etag)
            for k, v in extra:
                self.send_header(k, v)
            self._common_headers()
            self.send_header("Cache-Control", cache)
            self.end_headers()
            self.wfile.write(data)

        def _static_file(self, path: Path, content_type: str, cache: str) -> None:
            found = _static(path)
            if found is None:
                return self._json(404, {"error": "not found"})
            raw, gz, etag = found
            return self._bytes(200, raw, content_type, cache=cache, gz=gz, etag=etag)

        def _token(self) -> str | None:
            from http.cookies import CookieError, SimpleCookie

            from .classroom import COOKIE

            try:
                jar = SimpleCookie(self.headers.get("Cookie", ""))
            except CookieError:
                return None
            morsel = jar.get(COOKIE)
            return morsel.value if morsel else None

        def _classroom_auth(self, method: str, path: str):
            """Handle login/logout/me; return the user's context, or None when answered."""
            from .classroom import COOKIE, SESSION_TTL

            ip = self.client_address[0]
            if method == "POST" and path == "/api/login":
                try:
                    body = self._read_body()
                except ValueError:
                    return self._json(413, {"error": "too large"})
                code, payload, token = classroom.login(body.get("username"), body.get("password"), ip,
                                                       create=body.get("create") is True)
                cookie = None
                if token:
                    cookie = f"{COOKIE}={token}; HttpOnly; SameSite=Strict; Path=/; Max-Age={SESSION_TTL}"
                return self._json(code, payload, cookie=cookie)
            token = self._token()
            if method == "POST" and path == "/api/logout":
                classroom.logout(token)
                return self._json(200, {"ok": True}, cookie=f"{COOKIE}=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0")
            user = classroom.sessions.user_for(token)
            if not user:
                return self._json(401, {"error": "login required", "classroom": True, "signup": classroom.signup})
            if path == "/api/me":
                return self._json(200, {"classroom": True, "user": user, "signup": classroom.signup,
                                        "sync": classroom.sync is not None})
            return classroom.ctx(user)

        def do_GET(self) -> None:  # noqa: N802
            path = urlparse(self.path).path
            if classroom is None or not path.startswith("/api/"):
                if path == "/api/me":
                    return self._json(200, {"classroom": False})
                return self._do_get(engine)
            ctx = self._classroom_auth("GET", path)
            if ctx is None:
                return None
            with ctx.lock:
                return self._do_get(ctx.engine)

        def do_POST(self) -> None:  # noqa: N802
            try:
                self._unread = max(0, int(self.headers.get("Content-Length", "0")))
            except ValueError:
                self._unread = 0
            try:
                return self._post()
            finally:
                if self._unread:  # answered without reading the body (e.g. 401): don't reuse this connection
                    self.close_connection = True

        def _post(self) -> None:
            path = urlparse(self.path).path
            ctx = None
            if classroom is not None:
                ctx = self._classroom_auth("POST", path)
                if ctx is None:
                    return None
            if path == "/api/restore":
                return self._restore(engine if ctx is None else ctx.engine, ctx)
            try:
                body = self._read_body()
            except ValueError:
                return self._json(413, {"error": "request body too large"})
            if ctx is None:
                return self._do_post(engine, body)
            with ctx.lock:
                return self._do_post(ctx.engine, body)

        def _restore(self, engine: AcademyEngine, ctx):
            if classroom is not None:
                return self._json(403, {"ok": False, "error": "Your instructor keeps classroom progress. Ask them to restore a save file."})
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                length = 0
            if length <= 0:
                return self._json(400, {"ok": False, "error": "Choose a save file first."})
            if length > MAX_SAVE_FILE:
                return self._json(413, {"ok": False, "error": "That file is too large to be a save file."})
            raw = self.rfile.read(length)
            self._unread = 0
            try:
                return self._json(200, engine.restore_from(raw))
            except SaveFileError as exc:
                return self._json(400, {"ok": False, "error": str(exc)})

        def do_OPTIONS(self) -> None:  # noqa: N802
            self.send_response(204)
            self._common_headers()
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Content-Length", "0")
            self.end_headers()

        def _html_file(self, path: Path) -> None:
            if not path.is_file():
                return self._json(404, {"error": "ui missing"})
            # "no-cache" = check first: an unchanged page costs a 304, not the whole file.
            return self._static_file(path, "text/html; charset=utf-8", "no-cache")

        def _do_get(self, engine: AcademyEngine) -> None:
            parsed = urlparse(self.path)
            path = parsed.path
            store = engine.progress()

            if path in ("/", "/index.html", "/dojo"):
                return self._html_file(DOJO_HTML)
            if path in ("/admin", "/admin/"):
                if not _admin_on():
                    return self._json(403, {"error": "Admin mode is off. Start it with ACADEMY_ADMIN=1 ./run.sh and type the admin password."})
                return self._html_file(ADMIN_HTML)
            if path.startswith("/icons/"):
                # Offline icon pack (PNG). Keep paths under static/icons only.
                name = unquote(path[len("/icons/") :].lstrip("/"))
                if "/" in name or "\\" in name or name.startswith(".") or not name.endswith((".svg", ".png")):
                    return self._json(404, {"error": "not found"})
                icon = STATIC_DIR / "icons" / name
                if not icon.is_file():
                    return self._json(404, {"error": "not found"})
                ctype = "image/svg+xml" if name.endswith(".svg") else "image/png"
                return self._static_file(icon, ctype, STATIC_CACHE)
            if path.startswith("/fonts/"):
                name = unquote(path[len("/fonts/") :].lstrip("/"))
                if "/" in name or "\\" in name or name.startswith(".") or not name.endswith((".woff2", ".woff")):
                    return self._json(404, {"error": "not found"})
                font = STATIC_DIR / "fonts" / name
                if not font.is_file():
                    return self._json(404, {"error": "not found"})
                ctype = "font/woff2" if name.endswith(".woff2") else "font/woff"
                return self._static_file(font, ctype, STATIC_CACHE)
            if path == "/api/admin/overview":
                denied = self._admin_required()
                if denied:
                    return denied
                return self._json(200, curriculum_overview(engine))
            if path == "/api/admin/feedback":
                denied = self._admin_required()
                if denied:
                    return denied
                return self._json(200, {"feedback": engine.feedback()})
            if path == "/api/admin/proposals":
                denied = self._admin_required()
                if denied:
                    return denied
                return self._json(200, list_proposals(engine.curriculum_root))
            if path.startswith("/api/admin/modules/"):
                denied = self._admin_required()
                if denied:
                    return denied
                slug = unquote(path[len("/api/admin/modules/") :].strip("/"))
                detail = module_detail(engine, slug)
                if detail is None:
                    return self._json(404, {"error": "module not found"})
                return self._json(200, detail)
            if path.startswith("/api/admin/challenges/draft"):
                denied = self._admin_required()
                if denied:
                    return denied

                qs = parse_qs(parsed.query or "")
                module_slug = (qs.get("module") or ["orientation"])[0]
                title = (qs.get("title") or [""])[0]
                return self._json(
                    200,
                    {"draft": default_challenge_draft(module_slug, title)},
                )
            if path == "/api/save":
                name = (parse_qs(parsed.query).get("name") or [""])[0]
                buf = io.BytesIO()
                engine.save_to(buf, name=name)
                data = buf.getvalue()
                self.send_response(200)
                self.send_header("Content-Type", "application/zip")
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Content-Disposition", f'attachment; filename="{default_filename()}"')
                self._common_headers()
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(data)
                return None
            if path == "/api/status":
                return self._json(200, engine.status_summary())
            if path == "/api/profile":
                from .dojos import profile_payload

                return self._json(200, profile_payload(engine))
            if path == "/api/dojos":
                return self._json(200, catalog_payload(engine))
            if path.startswith("/api/dojos/"):
                dojo_id = unquote(path[len("/api/dojos/") :].strip("/"))
                detail = dojo_detail(engine, dojo_id)
                if detail is None:
                    return self._json(404, {"error": "dojo not found"})
                return self._json(200, detail)
            if path == "/api/modules":
                modules = []
                for m in engine.modules:
                    chs = []
                    for c in engine.module_challenges(m.slug):
                        prog = store.challenges.get(c.id)
                        chs.append(
                            {
                                "id": c.id,
                                "title": display_title(c.id, c.title),
                                "difficulty": c.difficulty,
                                "estimated_time": c.estimated_time,
                                "solved": bool(prog and prog.solved),
                                "thumb": f"/api/thumbs/{c.id}.svg",
                            }
                        )
                    modules.append(
                        {
                            "slug": m.slug,
                            "title": m.title,
                            "order": m.order,
                            "description": m.description,
                            "challenges": chs,
                        }
                    )
                return self._json(200, modules)
            if path.startswith("/api/thumbs/"):
                cid = unquote(path[len("/api/thumbs/") :].strip("/"))
                if cid.endswith(".svg"):
                    cid = cid[: -len(".svg")]
                if not cid:
                    return self._json(404, {"error": "not found"})
                try:
                    engine.get_challenge(cid)
                except KeyError:
                    return self._json(404, {"error": "not found"})
                svg = challenge_thumb_svg(cid).encode("utf-8")
                return self._bytes(200, svg, "image/svg+xml; charset=utf-8", cache="private, max-age=86400")
            if path.startswith("/api/challenges/") and "/media/" in path:
                # Images a challenge's README/LESSON show in the reader: /api/challenges/<id>/media/<name>
                cid, _, name = path[len("/api/challenges/") :].partition("/media/")
                try:
                    c = engine.get_challenge(unquote(cid))
                except KeyError:
                    return self._json(404, {"error": "not found"})
                media = challenge_media(c, unquote(name))
                if media is None:
                    return self._json(404, {"error": "not found"})
                return self._bytes(200, *media)
            if path.startswith("/api/challenges/") and path.endswith("/docs"):
                try:
                    c = engine.get_challenge(path.split("/")[-2])
                except KeyError:
                    return self._json(404, {"error": "not found"})
                return self._json(200, {"docs": challenge_docs(c)})
            if path.startswith("/api/challenges/"):
                cid = path.split("/")[-1]
                try:
                    c = engine.get_challenge(cid)
                except KeyError:
                    return self._json(404, {"error": "not found"})
                prog = store.challenges.get(cid)
                return self._json(
                    200,
                    {
                        "id": c.id,
                        "title": display_title(c.id, c.title),
                        "module": c.module,
                        "difficulty": c.difficulty,
                        "estimated_time": c.estimated_time,
                        "prerequisites": c.prerequisites,
                        "objectives": c.objectives,
                        "description": c.description,
                        "expected_tools": c.expected_tools,
                        "hints_revealed": prog.hints_revealed if prog else 0,
                        "hints_total": len(c.hints or []),
                        "solved": bool(prog and prog.solved),
                        "current": store.current_challenge_id == cid,
                        "workspace": store.current_workspace if store.current_challenge_id == cid else None,
                    },
                )
            return self._json(404, {"error": "not found"})

        def _do_post(self, engine: AcademyEngine, body: dict) -> None:
            parsed = urlparse(self.path)

            if parsed.path == "/api/admin/challenges/validate":
                denied = self._admin_required()
                if denied:
                    return denied
                normalized = build_challenge_yaml(body)
                errors = validate_challenge_draft(normalized)
                return self._json(200, {"ok": not errors, "errors": errors, "normalized": normalized})

            if parsed.path == "/api/admin/toggle":
                denied = self._admin_required()
                if denied:
                    return denied
                enabled = body.get("enabled")
                if not isinstance(enabled, bool):
                    return self._json(400, {"ok": False, "error": "enabled must be true or false"})
                result = set_toggle(engine, str(body.get("kind", "")), str(body.get("id", "")), enabled)
                return self._json(200 if result["ok"] else 400, result)

            if parsed.path == "/api/admin/challenges/create":
                denied = self._admin_required()
                if denied:
                    return denied
                return self._json(200, create_challenge(engine, body))

            if parsed.path == "/api/admin/proposals":
                denied = self._admin_required()
                if denied:
                    return denied
                kind = str(body.get("kind", "challenge")).strip()
                title = str(body.get("title", "Untitled")).strip() or "Untitled"
                notes = str(body.get("notes", "")).strip()
                payload = {k: v for k, v in body.items() if k not in ("kind", "title", "notes")}
                return self._json(200, save_proposal(engine.curriculum_root, kind=kind, title=title, body=payload, notes=notes))

            if parsed.path.startswith("/api/admin/proposals/") and parsed.path.endswith("/apply"):
                denied = self._admin_required()
                if denied:
                    return denied
                filename = unquote(parsed.path[len("/api/admin/proposals/") : -len("/apply")].strip("/"))
                return self._json(200, apply_proposal(engine, filename))

            if parsed.path.endswith("/feedback") and parsed.path.startswith("/api/challenges/"):
                cid = parsed.path.split("/")[-2]
                try:
                    engine.record_feedback(cid, str(body.get("rating") or ""), str(body.get("note") or ""))
                except KeyError:
                    return self._json(404, {"error": "not found"})
                except ValueError as exc:
                    return self._json(400, {"error": str(exc)})
                return self._json(200, {"ok": True})

            if parsed.path.endswith("/hint"):
                cid = parsed.path.split("/")[-2]
                try:
                    level, text = engine.get_hint(cid)
                    revealed = [t for _, t in engine.list_revealed_hints(cid)]
                    total = len(engine.get_challenge(cid).hints)
                except KeyError:
                    return self._json(404, {"error": "not found"})
                # The page shows the whole list each time, so pressing Hint again never repeats one.
                return self._json(200, {"level": level, "text": text, "hints": revealed, "total": total})

            if parsed.path.endswith("/submit"):
                cid = parsed.path.split("/")[-2]
                flag = (body.get("flag") or "").strip()
                try:
                    engine.get_challenge(cid)
                except KeyError:
                    return self._json(404, {"error": "not found"})
                if not flag:
                    try:
                        return self._json(200, _run_workspace_check(engine, cid))
                    except Exception as exc:  # noqa: BLE001
                        return self._json(500, {"ok": False, "error": f"Check crashed: {exc}"})
                try:
                    ok = engine.submit(cid, flag)
                except KeyError:
                    return self._json(404, {"error": "not found"})
                payload = {"ok": ok, "via": "flag"}
                if ok:
                    ch = engine.get_challenge(cid)
                    payload["explanation"] = ch.explanation
                else:
                    payload["error"] = "Wrong flag — try again or take a hint."
                return self._json(200, payload)

            if parsed.path.endswith("/check"):
                cid = parsed.path.split("/")[-2]
                try:
                    engine.get_challenge(cid)
                except KeyError:
                    return self._json(404, {"error": "not found"})
                try:
                    return self._json(200, _run_workspace_check(engine, cid))
                except Exception as exc:  # noqa: BLE001 — keep HTTP connection alive
                    return self._json(500, {"ok": False, "error": f"Check crashed: {exc}"})

            if parsed.path.endswith("/start"):
                cid = parsed.path.split("/")[-2]
                open_term = body.get("open_terminal", True)
                if isinstance(open_term, str):
                    open_term = open_term.strip().lower() not in {"0", "false", "no", "off"}
                try:
                    dest = engine.start_challenge(cid)
                except (KeyError, RuntimeError) as exc:
                    return self._json(400, {"ok": False, "error": str(exc)})
                except Exception as exc:  # noqa: BLE001
                    return self._json(500, {"ok": False, "error": f"Start failed: {exc}"})
                payload = {
                    "ok": True,
                    "workspace": str(dest),
                    "challenge_id": cid,
                    "terminal": None,
                    # Logged-in learners: ~/signal-dojo/<name>, a short link to the folder above.
                    "shortcut": getattr(engine, "workspace_link", None),
                }
                # Classroom: only when the browser runs on the server itself; remote learners get the path.
                if open_term and (classroom is None or ipaddress.ip_address(self.client_address[0]).is_loopback):
                    payload["terminal"] = open_workspace_terminal(dest, challenge_id=cid)
                return self._json(200, payload)

            return self._json(404, {"error": "not found", "path": parsed.path})

        def log_message(self, fmt: str, *args) -> None:
            pass

    try:
        httpd = ThreadingHTTPServer((host, port), Handler)
    except OSError as e:
        if e.errno == errno.EADDRINUSE:
            raise SystemExit(port_in_use_message(port)) from None
        raise
    httpd.daemon_threads = True
    httpd.serve_forever()
