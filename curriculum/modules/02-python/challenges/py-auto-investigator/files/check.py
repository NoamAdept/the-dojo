#!/usr/bin/env python3
import os
from pathlib import Path

def fail(message):
    print("Not yet:", message)
    raise SystemExit(1)

import importlib.util, json, tempfile
s=importlib.util.spec_from_file_location("student","investigate.py"); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
with tempfile.TemporaryDirectory() as td:
    inp=Path(td)/"in.csv"; out=Path(td)/"out.json"
    inp.write_text("time,station,snr,status\n1,ZED,1,LOCKED\n2,ZED,2,LOCKED\n3,ZED,6,LOCKED\n4,ANN,9,LOCKED\n5,ANN,99,SEARCHING\n6,BOB,4,LOCKED\n7,BOB,8,LOCKED\n")
    m.investigate(inp,out)
    if not out.exists(): fail("investigate must write the file at output_path")
    got=json.loads(out.read_text())
    if got != {"ZED":{"count":3,"average_snr":3.0}}:
        fail("use only LOCKED rows, keep stations with 3 or more, and round the average to 1 decimal")

flag_path = Path(Path(".flagpath").read_text().strip()) if Path(".flagpath").exists() else Path(os.environ.get("ACADEMY_FLAG_PATH", "/home/flag.txt"))
flag_path.parent.mkdir(parents=True, exist_ok=True)
flag_path.write_text('')
print('CHECK_OK')
