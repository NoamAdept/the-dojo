"""Stage a challenge the way `Start` does, apply an answer, run its ./check, read the result.

Used by test_challenge_answers.py. Mirrors scripts/verify_answers.py, but reports which
task numbers pass so one ./check run can try a different answer for every task at once.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CURRICULUM = ROOT / "curriculum"
TIMEOUT = 300


@dataclass
class Result:
    ok: bool
    output: str
    failing: set[int] = field(default_factory=set)  # task numbers listed under "Not yet:"

    def task_passes(self, n: int) -> bool:
        return self.ok or n not in self.failing


class Lab:
    """One engine with every challenge unlocked; stage() gives a fresh workspace each call."""

    def __init__(self) -> None:
        from academy.engine import AcademyEngine
        from academy.progress import ChallengeProgress

        self.tmp = Path(tempfile.mkdtemp(prefix="answer-tests-"))
        self.engine = AcademyEngine(
            curriculum_root=CURRICULUM, data_dir=self.tmp / "data",
            workspace_root=self.tmp / "ws", flag_path=self.tmp / "flag.txt",
        )
        store = self.engine.progress()
        for cid in self.engine._challenges:
            store.challenges.setdefault(cid, ChallengeProgress(started_at=0.0)).solved = True
        self.engine.progress_repo.save(store)
        self.count = 0
        self.env = os.environ.copy()
        self.env.pop("ACADEMY_ADMIN", None)
        self.env.update({
            "ACADEMY_FLAG_PATH": str(self.tmp / "flag.txt"), "ACADEMY_DATA": str(self.tmp / "data"),
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONPATH": os.pathsep.join(filter(None, [str(ROOT / "platform"), os.environ.get("PYTHONPATH")])),
        })

    def close(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def folder(self, cid: str) -> Path:
        return self.engine.get_challenge(cid).path.parent

    def stage(self, cid: str, *, solution: bool) -> Path:
        self.count += 1
        self.engine.workspace_root = self.tmp / "ws" / f"{cid}-{self.count}"
        ws = self.engine.start_challenge(cid)
        if solution:
            apply_solution(self.folder(cid) / "solution", ws)
            solve = self.folder(cid) / "solution" / "solve.sh"
            if solve.exists() and (ws / "check").exists():
                self.sh(ws, f"bash {solve}")
        return ws

    def sh(self, ws: Path, commands: str) -> subprocess.CompletedProcess:
        return subprocess.run(["bash", "-c", commands], cwd=ws, env={**self.env, "HOME": str(ws)},
                              stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=TIMEOUT)

    def check(self, ws: Path) -> Result:
        p = subprocess.run(["./check"], cwd=ws, env=self.env, stdin=subprocess.DEVNULL,
                           capture_output=True, text=True, timeout=TIMEOUT, errors="replace")
        out = p.stdout + p.stderr
        failing = {int(m) for m in re.findall(r"^\s+- (\d+)\b", out, re.M)}
        return Result("CHECK_OK" in out, out, failing)


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


def write_files(ws: Path, files: dict[str, str]) -> None:
    for rel, text in files.items():
        p = ws / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
