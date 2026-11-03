#!/usr/bin/env python3
import os
from pathlib import Path

def fail(message):
    print("Not yet:", message)
    raise SystemExit(1)

import re
src = Path("bulletin.txt").read_text()
expected = sorted(set(re.findall(r"(?<![\d.])(\d+\.\d+)\s+MHz", src)), key=float)
p = Path("frequencies.txt")
if not p.exists():
    fail("create frequencies.txt")
got = [x.strip() for x in p.read_text().splitlines() if x.strip()]
def numbers(lines):
    """145.800 and 145.8 are the same frequency."""
    try:
        return [float(x) for x in lines]
    except ValueError:
        return None
if numbers(got) != numbers(expected):
    fail("take out each MHz number only 1 time, and sort them as numbers")

flag_path = Path(Path(".flagpath").read_text().strip()) if Path(".flagpath").exists() else Path(os.environ.get("ACADEMY_FLAG_PATH", "/home/flag.txt"))
flag_path.parent.mkdir(parents=True, exist_ok=True)
flag_path.write_text('')
print('CHECK_OK')
