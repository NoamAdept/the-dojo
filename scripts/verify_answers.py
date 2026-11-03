#!/usr/bin/env python3
"""Prove every challenge's answer passes its own check.

For each challenge: stage a fresh copy exactly as `./academy start` does, confirm the
untouched starter does NOT pass, apply the answer from the challenge's `solution/`
folder, then run `./check` and require `CHECK_OK`.

The answer is applied in two steps:
  1. every file in `solution/` (except `solve.sh`) is copied over the workspace;
  2. `solution/solve.sh`, if present, runs inside the workspace (commands a learner
     types: mkdir, chmod, running a program, ...).

Challenges without a `./check` are flag hunts: `solve.sh` must print the flag it found
on its last line, and the engine must accept it.

    python3 scripts/verify_answers.py                 # everything
    python3 scripts/verify_answers.py pyq- lls-       # ids starting with these
    python3 scripts/verify_answers.py --json out.json # machine-readable report
    python3 scripts/verify_answers.py --classroom     # as a logged-in learner: one users/<name>/challenge
                                                      # folder reused for every challenge, HOME elsewhere

Before the answer is applied, every file in the challenge's `files/` folder must be in the
workspace at the same relative path with the same permissions, every name in `files:` must be
there, and the untouched starter's `./check` must not fail because a file it needs is missing.

Exit code 0 only when every selected challenge passes.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURRICULUM = Path(os.environ.get("ACADEMY_CURRICULUM", ROOT / "curriculum"))
sys.path.insert(0, str(ROOT / "platform"))

TIMEOUT = int(os.environ.get("VERIFY_TIMEOUT", "300"))
TASKS_RE = re.compile(r"(\d+)/(\d+) tasks? pass")
# What a check prints when a file it reads is not where it expects (the learner's "missing file").
MISSING_RE = re.compile(r"(No such file or directory|FileNotFoundError|cannot open|cannot access)[^\n]*")


def staging_problems(ch, ws: Path) -> list[str]:
    """Files Start should have put in the workspace but did not (or put with other permissions)."""
    probs = []
    src = ch.path.parent / "files"
    for path in sorted(src.rglob("*")) if src.is_dir() else []:
        if "__pycache__" in path.parts or not path.is_file():
            continue
        rel = path.relative_to(src)
        target = ws / rel
        if not target.exists() and rel.as_posix() not in ch.flags.plant_files:
            probs.append(f"missing after Start: {rel}")
        elif target.exists() and (path.stat().st_mode & 0o111) != (target.stat().st_mode & 0o111):
            probs.append(f"exec bit differs: {rel}")
    for name in ch.files:
        if not (ws / name).exists() and not (ws / name.rstrip("/")).exists():
            probs.append(f"listed in files: but not in the workspace: {name}")
    if (src / "check").is_file() and not os.access(src / "check", os.X_OK):
        probs.append("check is not executable")
    return probs


def run(cmd: list[str], cwd: Path, env: dict) -> tuple[int, str]:
    try:
        p = subprocess.run(
            cmd, cwd=cwd, env=env, stdin=subprocess.DEVNULL, capture_output=True,
            text=True, timeout=TIMEOUT, errors="replace",
        )
        return p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired as exc:
        out = (exc.stdout or b"") + (exc.stderr or b"")
        if isinstance(out, bytes):
            out = out.decode("utf-8", "replace")
        return 124, out + f"\n[timed out after {TIMEOUT}s]"


def apply_solution(solution: Path, ws: Path) -> None:
    for path in sorted(solution.rglob("*")):
        rel = path.relative_to(solution)
        if rel.as_posix() == "solve.sh" or "__pycache__" in rel.parts:
            continue
        target = ws / rel
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif path.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists() and not os.access(target, os.W_OK):
                target.chmod(target.stat().st_mode | 0o200)
            shutil.copy2(path, target)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prefixes", nargs="*", help="only challenge ids starting with one of these")
    ap.add_argument("--json", type=Path, help="write a JSON report here")
    ap.add_argument("--keep", action="store_true", help="keep the temp workspaces for debugging")
    ap.add_argument("--classroom", action="store_true",
                    help="stage like a logged-in learner (users/<name>/challenge, HOME elsewhere)")
    ap.add_argument("-v", "--verbose", action="store_true", help="print check output for failures")
    args = ap.parse_args()

    from academy.engine import AcademyEngine
    from academy.progress import ChallengeProgress

    tmp = Path(tempfile.mkdtemp(prefix="verify-answers-"))
    data_dir, ws_root = tmp / "data", tmp / "workspace"
    engine = AcademyEngine(
        curriculum_root=CURRICULUM, data_dir=data_dir, workspace_root=ws_root,
        flag_path=tmp / "flag.txt",
    )
    flag_path = tmp / "flag.txt"
    if args.classroom:
        # Exactly what `./run.sh` does for a learner who logged in: their own engine, one
        # challenge/ folder that every Start empties and refills, and a HOME that is not it.
        from academy.classroom import Classroom

        os.environ.setdefault("ACADEMY_WORKSPACE_LINKS", "0")  # no ~/dojo/learner link to a temp folder

        ctx = Classroom(engine, tmp / "pack" / ".academy-data" / "classroom").ctx("learner")
        engine, data_dir, flag_path = ctx.engine, ctx.engine.data_dir, ctx.flag
    # Mark everything solved so prerequisites never block staging.
    store = engine.progress()
    for cid in engine._challenges:
        store.challenges.setdefault(cid, ChallengeProgress(started_at=0.0)).solved = True
    engine.progress_repo.save(store)

    order = [ch for m in engine.modules for ch in engine.module_challenges(m.slug)]
    seen = {c.id for c in order}
    order += [c for c in engine._challenges.values() if c.id not in seen]
    if args.prefixes:
        order = [c for c in order if c.id.startswith(tuple(args.prefixes))]

    env = os.environ.copy()
    env.pop("ACADEMY_ADMIN", None)
    env["ACADEMY_FLAG_PATH"] = str(flag_path)
    if args.classroom:
        (tmp / "home").mkdir()
        env["HOME"] = str(tmp / "home")
    env["ACADEMY_DATA"] = str(data_dir)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    # Some checkers read their sealed answer through the academy package, as `./academy` would.
    env["PYTHONPATH"] = os.pathsep.join(filter(None, [str(ROOT / "platform"), env.get("PYTHONPATH")]))

    results = []
    for ch in order:
        t0 = time.time()
        folder = ch.path.parent
        solution = folder / "solution"
        res = {"id": ch.id, "module": ch.module, "status": "FAIL", "detail": "", "tasks": None, "baseline": None}
        try:
            # Each challenge gets its own workspace so nothing leaks between runs.
            if not args.classroom:
                engine.workspace_root = ws_root / ch.id
            ws = engine.start_challenge(ch.id)
            staged = staging_problems(ch, ws)
            if staged:
                raise RuntimeError("staging: " + "; ".join(staged))
            has_check = (ws / "check").exists()
            solve = solution / "solve.sh"
            if not solution.is_dir():
                res["detail"] = "no solution/ folder"
            elif has_check:
                code, out = run(["./check"], ws, env)
                res["baseline"] = "CHECK_OK" in out
                missing = MISSING_RE.search(out)
                if missing:
                    res["missing"] = missing.group(0)[:200]
                apply_solution(solution, ws)
                step = ["bash", str(solve)] if solve.exists() else None
                if step:
                    code, out = run(step, ws, env)
                    if code != 0:
                        raise RuntimeError(f"{step[-1]} exited {code}:\n{out[-1500:]}")
                code, out = run(["./check"], ws, env)
                m = TASKS_RE.findall(out)
                res["tasks"] = f"{m[-1][0]}/{m[-1][1]}" if m else None
                if "CHECK_OK" in out and not res["baseline"]:
                    res["status"] = "PASS"
                elif "CHECK_OK" in out:
                    res["detail"] = "starter already passes ./check (check does not test anything)"
                else:
                    res["detail"] = out.strip()[-1500:]
            elif solve.exists():
                apply_solution(solution, ws)
                code, out = run(["bash", str(solve)], ws, env)
                lines = [ln.strip() for ln in out.strip().splitlines() if ln.strip()]
                flag = lines[-1] if lines else ""
                if code == 0 and engine.submit(ch.id, flag):
                    res["status"] = "PASS"
                    res["tasks"] = "flag"
                else:
                    res["detail"] = f"engine rejected flag {flag!r} (solve.sh exit {code})\n{out[-1000:]}"
            else:
                res["detail"] = "no ./check and no solution/solve.sh"
        except Exception as exc:  # noqa: BLE001
            res["detail"] = f"{type(exc).__name__}: {exc}"
        res["seconds"] = round(time.time() - t0, 1)
        results.append(res)
        tag = res["status"] if res["status"] == "PASS" else "FAIL"
        print(f"{tag:4}  {ch.id:34} {res['tasks'] or '':6} {res['seconds']:5}s", flush=True)
        if res.get("missing"):
            print(f"      starter ./check hit a missing file: {res['missing']}")
        if tag != "PASS" and args.verbose:
            print("      " + res["detail"].replace("\n", "\n      "))

    passed = sum(r["status"] == "PASS" for r in results)
    print(f"\n{passed}/{len(results)} answers pass their check")
    for r in results:
        if r["status"] != "PASS":
            print(f" - {r['id']}: {r['detail'].splitlines()[-1] if r['detail'] else ''}")
    if args.json:
        args.json.write_text(json.dumps({"passed": passed, "total": len(results), "results": results}, indent=2))
    if not args.keep:
        shutil.rmtree(tmp, ignore_errors=True)
    else:
        print(f"workspaces kept in {tmp}")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
