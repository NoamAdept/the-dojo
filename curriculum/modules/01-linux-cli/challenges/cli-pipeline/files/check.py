#!/usr/bin/env python3
import os
from pathlib import Path

def fail(message):
    print("Not yet:", message)
    raise SystemExit(1)

import csv
answer = Path("answer.txt")
if not answer.exists():
    fail("create answer.txt")
rows = list(csv.DictReader(Path("readings.csv").open()))
expected = [r["callsign"] for r in sorted((r for r in rows if r["region"] == "north"), key=lambda r: int(r["strength"]), reverse=True)[:3]]
got = [line.strip() for line in answer.read_text().splitlines() if line.strip()]
if got != expected:
    fail("answer.txt must list the 3 northern callsigns, 1 per line, strongest first")

flag_path = Path(Path(".flagpath").read_text().strip()) if Path(".flagpath").exists() else Path(os.environ.get("ACADEMY_FLAG_PATH", "/home/flag.txt"))
flag_path.parent.mkdir(parents=True, exist_ok=True)
flag_path.write_text('')
print('CHECK_OK')
