"""Make `python3 -m pytest platform/tests` work from a plain checkout (no pip install)."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for p in (ROOT / "vendor", ROOT / "platform"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import os

# Classroom logins add ~/dojo/<name> links; tests must not touch the real home folder.
os.environ.setdefault("ACADEMY_WORKSPACE_LINKS", "0")
