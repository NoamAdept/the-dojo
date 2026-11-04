"""docs/answers/<id>.md is written from each challenge's solution/ folder: keep the two in step."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_answer_pages_match_the_solutions():
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "build_answers_guide.py"), "--check"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
