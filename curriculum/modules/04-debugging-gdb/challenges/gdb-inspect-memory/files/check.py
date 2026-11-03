#!/usr/bin/env python3
import os, re, subprocess, tempfile
from pathlib import Path

def fail(message):
    print("Not yet:", message)
    raise SystemExit(1)

p=Path("answer.txt")
if not p.exists(): fail("create answer.txt")
expected=bytes([0xaa,0x55,3,0x10,0,0xfe,1,0xef])
# The bytes count, not the spelling: "aa 55 03 ...", "0xaa 0x55 ...", "AA,55,...", "aa5503...",
# or gdb's whole x/8bx line with the address in front are all fine.
text=p.read_text().strip().lower().replace("0x","")
text=text.rsplit(":",1)[-1]
parts=[x for x in re.split(r"[\s,]+",text) if x]
if len(parts)==1 and len(parts[0])==16: parts=re.findall("..",parts[0])
try: got=bytes(int(x,16) for x in parts) if all(len(x)<=2 for x in parts) else None
except ValueError: got=None
if got!=expected: fail("use x/8bx packet, then write all 8 bytes as hex, like aa 55 ...")

flag_path = Path(Path(".flagpath").read_text().strip()) if Path(".flagpath").exists() else Path(os.environ.get("ACADEMY_FLAG_PATH", "/home/flag.txt"))
flag_path.parent.mkdir(parents=True, exist_ok=True)
flag_path.write_text('')
print('CHECK_OK')
