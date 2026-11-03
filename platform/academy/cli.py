"""CLI entrypoint — offline CTF lab console."""

from __future__ import annotations

import argparse
import os
import shlex
import sys
import textwrap
import time
from pathlib import Path

from . import __version__
from .engine import AcademyEngine
from .models import Challenge


WIDTH = 72
USE_COLOR = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None


class C:
    reset = "\033[0m"
    dim = "\033[2m"
    bold = "\033[1m"
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    cyan = "\033[36m"
    magenta = "\033[35m"


def _c(code: str, text: str) -> str:
    if not USE_COLOR:
        return text
    return f"{code}{text}{C.reset}"


def _tag(kind: str) -> str:
    styles = {
        "*": (C.cyan, "[*]"),
        "+": (C.green, "[+]"),
        "-": (C.red, "[-]"),
        "!": (C.yellow, "[!]"),
        ">": (C.magenta, "[>]"),
        "=": (C.dim, "[=]"),
        "?": (C.yellow, "[?]"),
    }
    color, label = styles.get(kind, (C.dim, f"[{kind}]"))
    return _c(color, label)


def _diff(level: str) -> str:
    colors = {"easy": C.green, "medium": C.yellow, "hard": C.red}
    return _c(colors.get(level, C.dim), level)


def _paths() -> tuple[Path, Path]:
    curriculum = Path(
        os.environ.get(
            "ACADEMY_CURRICULUM",
            str(Path(__file__).resolve().parents[2] / "curriculum"),
        )
    )
    data_dir = Path(os.environ.get("ACADEMY_DATA", str(Path.home() / ".academy")))
    return curriculum, data_dir


def _engine() -> AcademyEngine:
    curriculum, data_dir = _paths()
    user = os.environ.get("ACADEMY_USER", "").strip().lower()
    if user:
        # A logged-in learner's own folder (what ./run.sh serves): ACADEMY_USER=maya ./academy hint
        from .classroom import valid_username

        if not valid_username(user):
            raise SystemExit(f"ACADEMY_USER={user!r} is not a valid username")
        root = data_dir / "classroom" / "users" / user
        if not root.is_dir():
            raise SystemExit(f"No learner {user!r} here yet: log in once in the browser first ({root})")
        return AcademyEngine(
            curriculum_root=curriculum, data_dir=root / ".academy",
            workspace_root=root / "challenge", flag_path=root / "flag.txt",
        )
    return AcademyEngine(curriculum_root=curriculum, data_dir=data_dir)


def _format_body(text: str) -> str:
    """Preserve structure; wrap only ordinary prose lines."""
    out: list[str] = []
    in_code = False
    for raw in text.strip().splitlines():
        line = raw.rstrip()
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            out.append("  " + line)
            continue
        if not line:
            out.append("")
            continue
        if line.startswith("#"):
            title = line.lstrip("#").strip()
            out.append(title)
            out.append("-" * min(len(title), WIDTH))
            continue
        # Keep indented / command-like lines intact
        if line.startswith(" ") or line.startswith("\t") or line.startswith("```"):
            out.append(line)
            continue
        if line.startswith(("- ", "* ", "1.", "2.", "3.", "4.", "5.", "6.")):
            out.append(textwrap.fill(line, width=WIDTH, subsequent_indent="   "))
            continue
        out.append(textwrap.fill(line, width=WIDTH))
    # Collapse excessive blank lines
    cleaned: list[str] = []
    blank = 0
    for line in out:
        if line == "":
            blank += 1
            if blank <= 1:
                cleaned.append(line)
        else:
            blank = 0
            cleaned.append(line)
    return "\n".join(cleaned).strip()


def _resolve_challenge_id(eng: AcademyEngine, challenge_id: str | None) -> str:
    if challenge_id:
        return challenge_id
    current = eng.current_challenge()
    if current:
        return current.id
    nxt = eng.next_available_challenge()
    if nxt:
        raise RuntimeError(f"{_tag('!')} no active target — run: academy next")
    raise RuntimeError(f"{_tag('-')} no active target — try: academy status")


def print_challenge_briefing(ch: Challenge, dest: Path) -> None:
    print(f"{_tag('+')} challenge ready :: {_c(C.bold, ch.title)}")
    print(
        f"{_tag('=')} {ch.id}  "
        f"level={_diff(ch.difficulty)}  "
        f"time={ch.estimated_time}"
    )
    print()
    print(_format_body(ch.description))
    print()
    print(f"{_tag('*')} folder: {_c(C.cyan, str(dest))}")
    entries = sorted(
        (e for e in dest.iterdir() if not e.name.startswith(".")),
        key=lambda p: (not p.is_dir(), p.name.lower()),
    )
    shown = [e.name + ("/" if e.is_dir() else "") for e in entries[:12]]
    extra = len(entries) - 12
    files = ", ".join(shown) + (f", …+{extra}" if extra > 0 else "")
    if files:
        print(f"{_tag('*')} files: {files}")
    print()
    print(f"{_tag('>')} when done:  ./check")
    print("    " + _c(C.dim, "found a flag?  submit it in the dojo UI"))


def cmd_welcome(_args: argparse.Namespace | None = None) -> int:
    from .dojos import dojo_stats, load_dojos, next_dojo

    eng = _engine()
    summary = eng.status_summary()
    current = eng.current_challenge()
    nxt = eng.next_available_challenge()
    ws = eng.workspace_for()
    catalog = load_dojos(eng.curriculum_root)

    print(_c(C.bold, "╔══════════════════════════════════════════╗"))
    print(_c(C.bold, "║        The Dojo  ·  ONLINE            ║"))
    print(_c(C.bold, "╚══════════════════════════════════════════╝"))
    print(f"{_tag('*')} airgap online · earn your belts")
    print(f"{_tag('=')} score {_c(C.green, str(summary['solved']))}/{summary['total']} solved")
    print(f"{_tag('=')} challenge folder {_c(C.cyan, str(ws))}")
    print()
    if catalog.intro:
        print(_format_body(catalog.intro.split("\n\n")[0]))
        print()

    dojo = next_dojo(eng)
    if dojo:
        print(
            f"{_tag('>')} dojo: {_c(C.bold, dojo.title)}  "
            f"[{dojo.belt_label}]  {dojo.solved}/{dojo.challenges}"
        )
    if current and not eng.is_solved(current.id):
        print(f"{_tag('>')} current: {_c(C.bold, current.title)} ({current.id})")
        print("    resume:")
        print(f"      cd {shlex.quote(str(ws))}")
        print("      academy hint")
        print("      ./check")
    elif nxt:
        print(f"{_tag('>')} next: {_c(C.bold, nxt.title)} ({nxt.id})")
        print("    start:")
        print("      next")
        print(f"      cd {shlex.quote(str(ws))}")
    else:
        print(f"{_tag('+')} nothing left unlocked — status")

    print()
    print(f"{_tag('*')} belts")
    for d in dojo_stats(eng):
        if d.kind != "core":
            continue
        if d.locked:
            mark = _c(C.dim, "LCK")
        elif d.solved >= d.challenges and d.challenges:
            mark = _c(C.green, "PWN")
        else:
            mark = _c(C.yellow, "OPN")
        print(
            f"  [{mark}] {d.belt_label:<12} {d.title:<28} "
            f"{_c(C.green, str(d.solved))}/{d.challenges}"
        )

    print()
    print(f"{_tag('*')} commands")
    print("    next      start next challenge")
    print("    dojos     browse dojos / belts")
    print("    hint      get a hint")
    print("    ./check   grade + score (in challenge folder)")
    print("    status    show progress")
    print("    save      save progress + your files to one .zip (academy restore FILE brings it back)")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    from .dojos import dojo_stats

    eng = _engine()
    store = eng.progress()

    if args.module:
        # Allow listing by dojo id or module slug
        dojos = {d.id: d for d in dojo_stats(eng)}
        if args.module in dojos:
            d = dojos[args.module]
            print(f"{_tag('*')} dojo :: {d.title} [{d.belt_label}]")
            if d.tagline:
                print(f"    {d.tagline}")
            for slug in d.module_slugs:
                try:
                    module = eng.get_module(slug)
                except KeyError:
                    continue
                chs = eng.module_challenges(slug)
                solved = sum(1 for c in chs if eng.is_solved(c.id, store))
                print(
                    f"  {_c(C.cyan, slug):<24} "
                    f"{_c(C.green, str(solved))}/{len(chs)}  {module.title}"
                )
            print(f"{_tag('>')} list <module-slug>  |  next")
            return 0
        try:
            module = eng.get_module(args.module)
        except KeyError:
            print(f"{_tag('-')} unknown module/dojo '{args.module}'", file=sys.stderr)
            return 1
        print(f"{_tag('*')} module {module.order:02d} :: {module.title} [{module.slug}]")
        for ch in eng.module_challenges(args.module):
            solved = eng.is_solved(ch.id, store)
            locked = not solved and not eng.prerequisites_met(ch, store)
            if solved:
                mark = _c(C.green, "PWN")
            elif locked:
                mark = _c(C.dim, "LCK")
            else:
                mark = _c(C.yellow, "OPN")
            print(
                f"  [{mark}] {_diff(ch.difficulty):<14} "
                f"{ch.id:<28} {ch.title}"
            )
        print(f"{_tag('>')} next")
        return 0

    print(f"{_tag('*')} core dojos — earn your belts")
    for d in dojo_stats(eng):
        if d.kind != "core":
            continue
        if d.locked:
            mark = _c(C.dim, "LCK")
        elif d.solved >= d.challenges and d.challenges:
            mark = _c(C.green, "PWN")
        else:
            mark = _c(C.yellow, "OPN")
        print(
            f"  [{mark}] {d.belt_label:<12} {_c(C.cyan, d.id):<22} "
            f"{_c(C.green, str(d.solved))}/{d.challenges}  {d.title}"
        )
    sides = [d for d in dojo_stats(eng) if d.kind != "core"]
    if sides:
        print()
        print(f"{_tag('*')} side quests")
    for d in sides:
        mark = (
            _c(C.green, "PWN")
            if d.challenges and d.solved >= d.challenges
            else _c(C.yellow, "OPN")
        )
        print(
            f"  [{mark}] {d.belt_label:<12} {_c(C.cyan, d.id):<22} "
            f"{_c(C.green, str(d.solved))}/{d.challenges}  {d.title}"
        )
    print(f"{_tag('>')} list intro-lab  |  list orientation")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    eng = _engine()
    try:
        ch = eng.get_challenge(args.challenge_id)
    except KeyError:
        print(f"{_tag('-')} unknown target '{args.challenge_id}'", file=sys.stderr)
        return 1
    print_challenge_briefing(ch, eng.workspace_for())
    return 0


def cmd_start(args: argparse.Namespace) -> int:
    eng = _engine()
    try:
        dest = eng.start_challenge(args.challenge_id, reset=not args.keep)
        ch = eng.get_challenge(args.challenge_id)
    except KeyError:
        print(f"{_tag('-')} unknown target '{args.challenge_id}'", file=sys.stderr)
        return 1
    except RuntimeError as exc:
        print(f"{_tag('-')} {exc}", file=sys.stderr)
        return 1
    print_challenge_briefing(ch, dest)
    return 0


def cmd_next(_args: argparse.Namespace) -> int:
    eng = _engine()
    nxt = eng.next_available_challenge()
    if nxt is None:
        summary = eng.status_summary()
        if summary["solved"] >= summary["total"]:
            print(f"{_tag('+')} curriculum pwned. you own the box.")
            return 0
        print(f"{_tag('!')} no unlocked targets — academy status")
        return 1
    try:
        dest = eng.start_challenge(nxt.id)
    except RuntimeError as exc:
        print(f"{_tag('-')} {exc}", file=sys.stderr)
        return 1
    print_challenge_briefing(nxt, dest)
    return 0


def cmd_hint(args: argparse.Namespace) -> int:
    eng = _engine()
    try:
        cid = _resolve_challenge_id(eng, args.challenge_id)
        level, text = eng.get_hint(cid)
    except (KeyError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if text is None:
        print(f"{_tag('-')} no intel left on this target")
        return 1
    ch = eng.get_challenge(cid)
    print(f"{_tag('?')} intel leak {level}/{len(ch.hints)} :: {ch.title}")
    print(_format_body(text))
    return 0


def _celebrate(title: str) -> None:
    """Short terminal celebration on flag capture."""
    if sys.stdout.isatty():
        for sp in ("·", "*", "✦", "✧", "*", "·"):
            line = f"  {sp}  {_c(C.green, '★ FLAG CAPTURED ★')}  {sp}  {_c(C.dim, title)}"
            sys.stdout.write("\r" + line + " " * 6)
            sys.stdout.flush()
            time.sleep(0.07)
        sys.stdout.write("\r" + " " * (WIDTH + 6) + "\r")
        sys.stdout.flush()

    name = (title or "target")[:34].center(34)
    banner = "\n".join(
        [
            "╔══════════════════════════════════════╗",
            "║                                      ║",
            "║       ★★  FLAG CAPTURED  ★★          ║",
            f"║  {name}  ║",
            "║                                      ║",
            "╚══════════════════════════════════════╝",
            "     *   .  ✦  .   *",
            "   .   ★ pwned ★   .",
            "     *   .  ✧  .   *",
        ]
    )
    print(_c(C.green, banner))
    print()


def _workspace(eng: AcademyEngine) -> Path:
    store = eng.progress()
    if store.current_workspace:
        return Path(store.current_workspace)
    return eng.workspace_for()


def _find_check(ws: Path) -> Path | None:
    for name in ("checker.py", "check.py"):
        candidate = ws / name
        if candidate.exists():
            return candidate
    check = ws / "check"
    if check.exists():
        return check
    return None


def _run_check_and_award(ws: Path, *, quiet: bool = False) -> str | None:
    """Run ./check; on success award sealed flag and return it. None if no check."""
    import subprocess

    from .grading import award_flag
    from .paths import resolve_flag_path

    check = _find_check(ws)
    if check is None:
        return None

    env = os.environ.copy()
    env["ACADEMY_WORKSPACE"] = str(ws)
    _curriculum, data_dir = _paths()
    env["ACADEMY_DATA"] = str(data_dir)
    env["ACADEMY_FLAG_PATH"] = str(resolve_flag_path())
    env["PYTHONPATH"] = str(Path(__file__).resolve().parent.parent) + (
        os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else ""
    )

    if check.name.endswith(".py") or check.suffix == ".py":
        cmd = [sys.executable, str(check)]
    elif os.access(check, os.X_OK):
        cmd = [str(check)]
    else:
        cmd = ["bash", str(check)]

    if not quiet:
        print(f"{_tag('*')} checking …", flush=True)
    result = subprocess.run(cmd, cwd=str(ws), env=env, check=False)
    if result.returncode != 0:
        print(f"{_tag('-')} not ready yet (check exit {result.returncode})")
        raise SystemExit(result.returncode or 1)

    return award_flag(ws, silent=True)


def cmd_verify(_args: argparse.Namespace) -> int:
    """Alias: same as bare academy submit (kept for old muscle memory)."""
    return cmd_submit(argparse.Namespace(challenge_id=None, flag=None))


def cmd_award(_args: argparse.Namespace) -> int:
    """Advanced: write sealed flag without submitting."""
    from .grading import award_flag

    eng = _engine()
    ws = _workspace(eng)
    try:
        award_flag(ws)
    except Exception as exc:  # noqa: BLE001
        print(f"{_tag('-')} {exc}", file=sys.stderr)
        return 1
    return 0


def cmd_submit(args: argparse.Namespace) -> int:
    """
    One-shot score:
      academy submit              → run ./check if needed, then submit
      academy submit 'flag{...}'  → submit a found flag
    """
    from .paths import read_flag_file, resolve_flag_path, write_flag_file

    eng = _engine()
    challenge_id = args.challenge_id
    flag = args.flag
    ws = _workspace(eng)

    # academy submit 'flag{...}'
    if flag is None and challenge_id and challenge_id.startswith("flag{"):
        flag = challenge_id
        challenge_id = None
    # academy submit /path/to/file
    elif flag is None and challenge_id and (
        challenge_id.endswith(".txt")
        or challenge_id.startswith("/")
        or challenge_id.startswith("~")
    ):
        path = Path(challenge_id).expanduser()
        flag = read_flag_file(path)
        challenge_id = None
        if not flag:
            print(f"{_tag('-')} no flag found in {path}", file=sys.stderr)
            return 1

    # Bare submit: flag file → else (already checked) award → else auto-check
    if flag is None:
        flag = read_flag_file(resolve_flag_path())
        if not flag and os.environ.get("ACADEMY_ALREADY_CHECKED") == "1":
            from .grading import award_flag

            try:
                flag = award_flag(ws, silent=True)
            except Exception as exc:  # noqa: BLE001
                print(f"{_tag('-')} {exc}", file=sys.stderr)
                return 1
        elif not flag and ws.exists() and _find_check(ws):
            try:
                flag = _run_check_and_award(ws)
            except SystemExit as exc:
                return int(exc.code) if isinstance(exc.code, int) else 1
        if not flag:
            print(
                f"{_tag('-')} nothing to submit yet\n"
                f"    Finish the work, then:  ./check\n"
                f"    Or paste a found flag:  academy submit 'flag{{...}}'",
                file=sys.stderr,
            )
            return 1

    try:
        cid = _resolve_challenge_id(eng, challenge_id)
        ok = eng.submit(cid, flag)
        ch = eng.get_challenge(cid)
    except (KeyError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if ok:
        try:
            write_flag_file(flag)
        except OSError:
            pass
        _celebrate(ch.title)
        if ch.explanation.strip():
            print(f"{_tag('*')} what you learned")
            print(_format_body(ch.explanation))
        nxt = eng.next_available_challenge()
        if nxt:
            print(f"\n{_tag('>')} next: {nxt.id} — run:  next")
        else:
            print(f"\n{_tag('+')} nothing left unlocked — run:  status")
        return 0

    print(f"{_tag('-')} wrong flag. try again — or: academy hint")
    return 1


def cmd_status(_args: argparse.Namespace) -> int:
    eng = _engine()
    summary = eng.status_summary()
    print(f"{_tag('*')} scoreboard  {_c(C.green, str(summary['solved']))}/{summary['total']} pwned")
    if summary.get("current_challenge_id"):
        print(f"{_tag('=')} active {summary['current_challenge_id']}")
    for module in eng.modules:
        info = summary["modules"][module.slug]
        if info["total"] == 0:
            continue
        print(
            f"  {module.order:02d}. {module.slug:<22} "
            f"{_c(C.green, str(info['solved']))}/{info['total']}"
        )
    nxt = eng.next_available_challenge()
    if nxt:
        print(f"{_tag('>')} next {nxt.id} → academy next")
    return 0


def cmd_where(_args: argparse.Namespace) -> int:
    eng = _engine()
    print(eng.workspace_for())
    return 0


def cmd_cd(_args: argparse.Namespace) -> int:
    eng = _engine()
    print(f"cd {shlex.quote(str(eng.workspace_for()))}")
    return 0


def cmd_save(args: argparse.Namespace) -> int:
    from .backup import default_filename

    eng = _engine()
    if args.file:
        out = Path(args.file).expanduser()
        if out.is_dir():
            out = out / default_filename()
    else:  # beside the challenge folder, which Start wipes
        out = eng.workspace_root.parent / default_filename()
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_name(out.name + ".part")
    with tmp.open("wb") as fh:
        summary = eng.save_to(fh)
    tmp.replace(out)
    print(f"{_tag('+')} saved {summary['solved']} solved challenges and your files from "
          f"{summary['challenges_with_files']} challenges")
    print(f"    {out}")
    print("    Copy it somewhere safe (a USB stick). Bring it back with:  academy restore FILE")
    return 0


def cmd_restore(args: argparse.Namespace) -> int:
    from .backup import SaveFileError

    eng = _engine()
    path = Path(args.file).expanduser()
    try:
        with path.open("rb") as fh:
            summary = eng.restore_from(fh)
    except OSError as exc:
        print(f"{_tag('-')} cannot read {path}: {exc.strerror or exc}", file=sys.stderr)
        return 1
    except SaveFileError as exc:
        print(f"{_tag('-')} {exc}", file=sys.stderr)
        return 1
    print(f"{_tag('+')} restored: {summary['solved']} solved ({summary['newly_solved']} new), "
          f"your files from {summary['challenges_with_files']} challenges")
    print("    Your files come back in the challenge folder when you start that challenge.")
    return 0


def cmd_docs(args: argparse.Namespace) -> int:
    from .docs_server import serve_docs

    docs_root = Path(
        os.environ.get(
            "ACADEMY_DOCS",
            str(Path(__file__).resolve().parents[2] / "docs"),
        )
    )
    print(f"{_tag('+')} intel server http://{args.host}:{args.port}/  (Ctrl+C gtfo)")
    serve_docs(docs_root, host=args.host, port=args.port)
    return 0


def cmd_serve(args: argparse.Namespace) -> int:
    from .api import serve_api

    from .admin_auth import first_run_setup

    curriculum, data_dir = _paths()
    first_run_setup(data_dir)  # interactive terminals only; never blocks a learner
    if args.local:  # SINGLE_USER=1 ./run.sh: one learner, one ./challenge folder, their own terminal
        print(f"{_tag('+')} console http://{args.host}:{args.port}/  (Ctrl+C gtfo)")
        serve_api(curriculum, data_dir, host=args.host, port=args.port)
        return 0

    from .classroom import Classroom, ProgressSync

    admin_data = data_dir  # where the admin page saves its on/off switches
    data_dir = _classroom_data(args, data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    sync = None
    if args.progress_repo:
        try:
            sync = ProgressSync(Path(args.progress_repo).expanduser())
        except (ValueError, OSError) as exc:
            print(f"{_tag('-')} {exc}", file=sys.stderr)
            return 2
    base = AcademyEngine(
        curriculum_root=curriculum,
        data_dir=data_dir,
        workspace_root=data_dir / "users",  # never used directly: each learner gets their own
        flag_path=data_dir / "users" / "unused-flag.txt",
    )
    from .toggles import FILENAME as TOGGLES_FILE, Toggles

    base.toggles = Toggles(admin_data / TOGGLES_FILE)  # dojos/challenges switched off on /admin stay off for the class
    classroom = Classroom(base, data_dir, signup=not args.no_signup, sync=sync)
    try:
        import getpass

        account = getpass.getuser()
    except Exception:  # noqa: BLE001
        account = "this account"
    print(f"{_tag('+')} classroom http://{args.host}:{args.port}/  (Ctrl+C gtfo)")
    if args.host in ("127.0.0.1", "localhost", "::1"):
        print(f"{_tag('!')} only this machine can connect. For the lab: academy serve --host <this machine's LAN IP>")
    print(f"{_tag('*')} data      {data_dir}  (accounts in users.json, learners in users/<name>/)")
    print(f"{_tag('*')} accounts  {'learners make their own account on the login page (Create account)' if not args.no_signup else 'admin-created only (academy user add NAME)'}")
    print(f"{_tag('*')} progress  {sync.repo if sync else 'local only (add --progress-repo PATH to share via git)'}")
    print(f"{_tag('!')} every learner folder belongs to OS user '{account}' — learners can read")
    print(f"{_tag('!')} each other's files and anything '{account}' can. Use a dedicated Pi / VM / container.")
    print(f"{_tag('!')} plain http: run only on a trusted lab network.")
    serve_api(curriculum, data_dir, host=args.host, port=args.port, classroom=classroom, base_engine=base)
    return 0


def _classroom_data(args: argparse.Namespace, data_dir: Path) -> Path:
    # Default: a classroom/ subfolder, so a single-user ./run.sh progress file never mixes with accounts.
    return Path(args.data).expanduser().resolve() if args.data else (data_dir / "classroom").resolve()


def cmd_user(args: argparse.Namespace) -> int:
    import getpass

    from .classroom import MIN_PASSWORD, USERNAME_RULE, UserStore, valid_username

    _, data_dir = _paths()
    data_dir = _classroom_data(args, data_dir)
    name = args.name.strip().lower()
    if not valid_username(name):
        print(f"{_tag('-')} username must be {USERNAME_RULE}", file=sys.stderr)
        return 2
    users = UserStore(data_dir / "users.json")
    exists = users.get(name) is not None
    if args.action == "add" and exists:
        print(f"{_tag('-')} {name} already exists (use: academy user passwd {name})", file=sys.stderr)
        return 1
    if args.action == "passwd" and not exists:
        print(f"{_tag('-')} no user {name} in {data_dir} (use: academy user add {name})", file=sys.stderr)
        return 1
    pw = getpass.getpass(f"Password for {name}: ")
    if len(pw) < MIN_PASSWORD:
        print(f"{_tag('-')} password must be at least {MIN_PASSWORD} characters", file=sys.stderr)
        return 1
    if getpass.getpass("Again: ") != pw:
        print(f"{_tag('-')} passwords differ", file=sys.stderr)
        return 1
    ok = users.create(name, pw) if args.action == "add" else users.set_password(name, pw)
    if not ok:
        print(f"{_tag('-')} could not save {name}", file=sys.stderr)
        return 1
    print(f"{_tag('+')} {'added' if args.action == 'add' else 'updated'} {name} in {data_dir / 'users.json'}")
    print(f"{_tag('*')} running servers pick this up on the next login")
    return 0


def cmd_admin(args: argparse.Namespace) -> int:
    from .admin_auth import password_file, require_admin, reset_password
    from .api import serve_api

    curriculum, data_dir = _paths()
    if args.reset_password:
        gone = reset_password(data_dir)
        print(f"{_tag('+')} admin password {'removed' if gone else 'was not set'} ({password_file(data_dir)})")
        print(f"{_tag('*')} the next admin run asks for a new one")
        return 0
    if args.change_password:
        from .admin_auth import has_password, prompt_new_password

        first = not has_password(data_dir)  # nothing to change yet: this sets the first one
        if not require_admin(data_dir):
            return 1
        return 0 if first or prompt_new_password(base=data_dir) else 1
    if not require_admin(data_dir):
        return 1
    url = f"http://{args.host}:{args.port}/admin"
    print(f"{_tag('+')} admin console {url}  (Ctrl+C gtfo)")
    print(f"{_tag('!')} student dojo still at http://{args.host}:{args.port}/dojo")
    serve_api(curriculum, data_dir, host=args.host, port=args.port, admin=True)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="academy",
        description="THE DOJO :: offline terminal, C++ and Python lab. Run plain 'academy'.",
    )
    parser.add_argument("--version", action="version", version=f"academy {__version__}")
    sub = parser.add_subparsers(dest="command")

    p_help = sub.add_parser("help", help="Ops guide")
    p_help.set_defaults(func=cmd_welcome)

    p_list = sub.add_parser("list", help="Recon modules / targets")
    p_list.add_argument("module", nargs="?", help="Module slug")
    p_list.set_defaults(func=cmd_list)

    p_show = sub.add_parser("show", help="Show target briefing")
    p_show.add_argument("challenge_id")
    p_show.set_defaults(func=cmd_show)

    p_start = sub.add_parser("start", help="Stage a target")
    p_start.add_argument("challenge_id")
    p_start.add_argument("--keep", action="store_true", help="Keep dropzone files")
    p_start.set_defaults(func=cmd_start)

    p_next = sub.add_parser("next", help="Stage next unlocked target")
    p_next.set_defaults(func=cmd_next)

    p_hint = sub.add_parser("hint", help="Leak intel")
    p_hint.add_argument("challenge_id", nargs="?")
    p_hint.set_defaults(func=cmd_hint)

    p_verify = sub.add_parser(
        "verify",
        help="Same as academy submit (alias)",
    )
    p_verify.set_defaults(func=cmd_verify)

    p_award = sub.add_parser(
        "award",
        help=argparse.SUPPRESS,  # advanced / internal
    )
    p_award.set_defaults(func=cmd_award)

    p_submit = sub.add_parser(
        "submit",
        help="Score the challenge (auto-runs ./check). Or: academy submit 'flag{...}'",
    )
    p_submit.add_argument(
        "challenge_id",
        nargs="?",
        help="Optional challenge id, flag string, or path to flag file",
    )
    p_submit.add_argument("flag", nargs="?", help="Optional flag string")
    p_submit.set_defaults(func=cmd_submit)

    p_status = sub.add_parser("status", help="Scoreboard")
    p_status.set_defaults(func=cmd_status)

    p_where = sub.add_parser("where", help="Print dropzone path")
    p_where.set_defaults(func=cmd_where)

    p_cd = sub.add_parser("cd", help='eval "$(academy cd)"')
    p_cd.set_defaults(func=cmd_cd)

    p_save = sub.add_parser("save", help="Save your progress and challenge files to one .zip")
    p_save.add_argument("file", nargs="?", help="where to write it (default: ~/dojo/the-dojo-save-DATE.zip)")
    p_save.set_defaults(func=cmd_save)

    p_restore = sub.add_parser("restore", help="Bring back progress and files from a save .zip")
    p_restore.add_argument("file")
    p_restore.set_defaults(func=cmd_restore)

    p_docs = sub.add_parser("docs", help="Offline intel server")
    p_docs.add_argument("--host", default="127.0.0.1")
    p_docs.add_argument("--port", type=int, default=8000)
    p_docs.set_defaults(func=cmd_docs)

    p_serve = sub.add_parser("serve", help="Classroom web server (logins + per-learner folders)")
    p_serve.add_argument("--host", default="127.0.0.1", help="IP to listen on, e.g. 192.168.1.50 or 0.0.0.0")
    p_serve.add_argument("--port", type=int, default=8080)
    p_serve.add_argument("--data", help="server data dir (accounts + every learner's folder)")
    p_serve.add_argument("--progress-repo", help="local git clone to commit/push progress/<user>.json into")
    p_serve.add_argument("--no-signup", action="store_true", help="only accounts made with: academy user add")
    p_serve.add_argument("--local", action="store_true", help="old single-user console (what ./run.sh uses)")
    p_serve.set_defaults(func=cmd_serve)

    p_user = sub.add_parser("user", help="Classroom accounts: academy user add|passwd NAME")
    p_user.add_argument("action", choices=["add", "passwd"])
    p_user.add_argument("name")
    p_user.add_argument("--data", help="server data dir (same as academy serve --data)")
    p_user.set_defaults(func=cmd_user)

    p_admin = sub.add_parser("admin", help="Curriculum admin UI (writes to curriculum/)")
    p_admin.add_argument("--host", default="127.0.0.1")
    p_admin.add_argument("--port", type=int, default=8080)
    p_admin.add_argument("--change-password", action="store_true", help="set a new admin password (asks for the old one)")
    p_admin.add_argument("--reset-password", action="store_true", help="forgot it: delete the admin password; the next run sets a new one")
    p_admin.set_defaults(func=cmd_admin)

    return parser


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        return cmd_welcome(None)
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        return cmd_welcome(None)
    from .admin import admin_requested

    classroom = args.command == "user" or (args.command == "serve" and not args.local)  # never admin
    if admin_requested() and args.command != "admin" and not classroom:  # e.g. ACADEMY_ADMIN=1 ./academy start <id>
        from .admin_auth import require_admin

        if not require_admin(_paths()[1]):
            return 1
    return args.func(args)


def main_next(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    return main(["next", *argv])


def main_hint(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    return main(["hint", *argv])


def main_submit(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    return main(["submit", *argv])


def main_status(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    return main(["status", *argv])


def main_list(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    return main(["list", *argv])


if __name__ == "__main__":
    raise SystemExit(main())
