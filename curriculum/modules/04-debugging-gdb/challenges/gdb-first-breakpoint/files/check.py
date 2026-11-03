#!/usr/bin/env python3
import os, re, subprocess, tempfile
from pathlib import Path

def fail(message):
    print("Not yet:", message)
    raise SystemExit(1)

p=Path("answer.txt")
if not p.exists(): fail("write the inspected decimal value to answer.txt")
expected=(17<<2)+5
# Accept the number alone, or gdb's own line for it: "$1 = 73" or "sample = 73".
m=re.fullmatch(r"(?:\$\d+\s*=\s*|[A-Za-z_]\w*\s*=\s*)?(-?\d+)", p.read_text().strip())
if not m: fail("answer.txt must contain one decimal integer")
got=int(m.group(1))
if got!=expected: fail("set a breakpoint at checkpoint, then print its sample argument")

flag_path = Path(Path(".flagpath").read_text().strip()) if Path(".flagpath").exists() else Path(os.environ.get("ACADEMY_FLAG_PATH", "/home/flag.txt"))
flag_path.parent.mkdir(parents=True, exist_ok=True)
flag_path.write_text('')
print('CHECK_OK')
