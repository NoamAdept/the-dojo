#!/usr/bin/env python3
"""Copy platform/academy/shellwords.py into every check.py that carries a copy of it.

Run after changing shellwords.py; platform/tests/test_shellwords.py fails until you do.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BEGIN, END = "# --- shellwords: begin", "# --- shellwords: end ---"


def block(text: str) -> str:
    return text[text.index(BEGIN):text.index(END) + len(END)]


new = block((ROOT / "platform/academy/shellwords.py").read_text())
for check in sorted(ROOT.glob("curriculum/modules/*/challenges/*/files/check.py")):
    text = check.read_text()
    if BEGIN in text and block(text) != new:
        check.write_text(text.replace(block(text), new))
        print("updated", check.relative_to(ROOT))
