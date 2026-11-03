#!/usr/bin/env python3
import os, re, subprocess, tempfile
from pathlib import Path

def fail(message):
    print("Not yet:", message)
    raise SystemExit(1)

p=Path("answer.txt")
if not p.exists(): fail("create answer.txt from the backtrace")
# C++ tools sometimes show a function with its parameter types, like capture(int)
# or main(). Both spellings are fine, so drop anything in brackets.
parts=[re.sub(r"\(.*\)$","",x.strip()).strip() for x in p.read_text().strip().split("->")]
if parts==["capture","demodulate","receive","main"]: fail("that is innermost first; write it from main (outermost) to capture (innermost)")
if parts!=["main","receive","demodulate","capture"]: fail("list every function in the backtrace, from main (outermost) to capture (innermost), joined by ->")

flag_path = Path(Path(".flagpath").read_text().strip()) if Path(".flagpath").exists() else Path(os.environ.get("ACADEMY_FLAG_PATH", "/home/flag.txt"))
flag_path.parent.mkdir(parents=True, exist_ok=True)
flag_path.write_text('')
print('CHECK_OK')
