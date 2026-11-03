#!/usr/bin/env python3
"""Run with ./check. Tests each task in tasks.py and lists what still fails."""
import sys
sys.path.insert(0, ".")
sys.dont_write_bytecode = True
failed, passed = [], []

def task(name):
    def run(fn):
        try:
            fn()
            passed.append(name)
        except NotImplementedError:
            failed.append(f"{name}: not implemented yet")
        except Exception as exc:  # show the learner what broke
            failed.append(f"{name}: {exc}" if isinstance(exc, AssertionError) and str(exc) else f"{name}: {type(exc).__name__}: {exc}")
        return fn
    return run

import os, struct, subprocess, sys, tempfile, tasks

@task("1 bit_state")
def _():
    assert tasks.bit_state(0b1001_0110, 4) == "ON" and tasks.bit_state(0b1001_0110, 3) == "OFF"

@task("2 clear_low_nibble")
def _():
    assert tasks.clear_low_nibble(0b1111_1111) == 0b1111_0000 and tasks.clear_low_nibble(0x1234) == 0x1230

@task("3 pack_reading")
def _():
    data = tasks.pack_reading(1, 2.5, 300)
    assert data == struct.pack("<Bfh", 1, 2.5, 300) and len(data) == 7

@task("4 endian_bytes")
def _():
    assert tasks.endian_bytes(0x12345678) == ("12345678", "78563412")

@task("5 count_set_bits")
def _():
    assert [tasks.count_set_bits(n) for n in (0, 1, 7, 0b1011, 2**64 - 1)] == [0, 1, 3, 3, 64]

@task("6 parse_packet")
def _():
    assert tasks.parse_packet(bytes.fromhex("aa55" "07" "deadbeef")) == (7, 0xDEADBEEF)
    for bad in (bytes.fromhex("aa56" "07" "deadbeef"), bytes.fromhex("aa55" "07")):
        try:
            tasks.parse_packet(bad)
        except ValueError:
            continue
        raise AssertionError(f"{bad.hex()} should raise ValueError")

@task("7 get_bmp_dimensions")
def _():
    d = tempfile.mkdtemp()
    subprocess.run([sys.executable, os.path.abspath("make_bmp.py")], cwd=d, check=True)
    assert tasks.get_bmp_dimensions(os.path.join(d, "pixel.bmp")) == (3, 2)
    bad = os.path.join(d, "bad.bmp")
    open(bad, "wb").write(b"XX" + bytes(60))
    try:
        tasks.get_bmp_dimensions(bad)
    except ValueError:
        pass
    else:
        raise AssertionError("non-BMP should raise ValueError")

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
