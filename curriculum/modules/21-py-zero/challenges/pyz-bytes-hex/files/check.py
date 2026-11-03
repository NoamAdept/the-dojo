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

import os, random, subprocess, tempfile

def load(name):
    try:
        return __import__(name)
    except Exception as exc:
        print(f"Could not load {name}.py. Python said: {type(exc).__name__}: {exc}")
        print(f"Run  python3 {name}.py  yourself to see the full error and its line number, fix it, then run ./check again.")
        raise SystemExit(1)

def same(got, want, call):
    if got is None and want is not None:
        raise AssertionError(f"{call} gave back None. Did you forget `return`, or use print() instead of return?")
    assert got == want, f"{call} returned {got!r}, but it should return {want!r}"

tasks = load("tasks")
rng = random.Random(10)

def rand_bytes(n):
    return bytes(rng.randrange(256) for _ in range(n))

@task("1 hex and binary")
def _():
    for n in [255, 26, 0, rng.randrange(256, 70000)]:
        same(tasks.to_hex(n), hex(n), f"to_hex({n})")
        same(tasks.to_binary(n), bin(n)[2:], f"to_binary({n})")
    for text in ["ff", "0x1a", "FF", format(rng.randrange(70000), "x")]:
        same(tasks.from_hex(text), int(text, 16), f"from_hex({text!r})")

@task("2 str and bytes")
def _():
    for text in ["Hi", "433.92 MHz", "pi-radio"]:
        same(tasks.text_to_bytes(text), text.encode(), f"text_to_bytes({text!r})")
        same(tasks.bytes_to_text(text.encode()), text, f"bytes_to_text({text.encode()!r})")
    got = tasks.text_to_bytes("ok")
    assert isinstance(got, bytes), f"text_to_bytes must return bytes (b'...'), not {type(got).__name__}. Use .encode()"

@task("3 hex text and bytes")
def _():
    same(tasks.parse_hex("48 69 21"), b"Hi!", "parse_hex('48 69 21')")
    data = rand_bytes(6)
    same(tasks.parse_hex(data.hex()), data, f"parse_hex({data.hex()!r})")
    same(tasks.show_hex(b"Hi!"), "486921", "show_hex(b'Hi!')")
    same(tasks.show_hex(data), data.hex(), f"show_hex({data!r})")

@task("4 bytes are ints")
def _():
    for data in [b"Hi!", rand_bytes(5), b"\x00\xff"]:
        same(tasks.byte_values(data), list(data), f"byte_values({data!r})")
        same(tasks.last_byte(data), data[-1], f"last_byte({data!r})")
    got = tasks.last_byte(b"AB")
    assert isinstance(got, int), f"last_byte must return an int, but you returned {got!r}. Index the bytes (data[-1]). Do not take a slice."

@task("5 two-byte numbers")
def _():
    same(tasks.read_u16(b"\x34\x12", 0), 0x1234, "read_u16(b'\\x34\\x12', 0)  (little-endian: low byte first)")
    same(tasks.read_i16(b"\xff\xff", 0), -1, "read_i16(b'\\xff\\xff', 0)  (use signed=True)")
    same(tasks.read_u16(b"\xff\xff", 0), 65535, "read_u16(b'\\xff\\xff', 0)  (unsigned: not negative)")
    data = rand_bytes(8)
    for pos in [0, 3, 6]:
        part = data[pos:pos + 2]
        same(tasks.read_u16(data, pos), int.from_bytes(part, "little"), f"read_u16({data!r}, {pos})")
        same(tasks.read_i16(data, pos), int.from_bytes(part, "little", signed=True), f"read_i16({data!r}, {pos})")

@task("6 struct")
def _():
    same(tasks.read_u16_struct(b"\x34\x12", 0), 0x1234, "read_u16_struct(b'\\x34\\x12', 0)")
    data = rand_bytes(9)
    for pos in [1, 4, 7]:
        same(tasks.read_u16_struct(data, pos), int.from_bytes(data[pos:pos + 2], "little"),
             f"read_u16_struct({data!r}, {pos})  (slice exactly 2 bytes and take [0] of the tuple)")

@task("7 xor checksum")
def _():
    same(tasks.xor_checksum(b"OK"), 0x4f ^ 0x4b, "xor_checksum(b'OK')")
    same(tasks.xor_checksum(b""), 0, "xor_checksum(b'')  (start from 0)")
    for n in [1, 7, 20]:
        data = rand_bytes(n)
        want = 0
        for b in data:
            want ^= b
        same(tasks.xor_checksum(data), want, f"xor_checksum({data!r})")

@task("8 walk a buffer")
def _():
    same(tasks.split_chunks(b"\x02hi\x03abc"), [b"hi", b"abc"], "split_chunks(b'\\x02hi\\x03abc')")
    same(tasks.split_chunks(b""), [], "split_chunks(b'')")
    chunks = [rand_bytes(rng.randrange(0, 6)) for _ in range(5)]
    buf = b"".join(bytes([len(c)]) + c for c in chunks)
    same(tasks.split_chunks(buf), chunks, f"split_chunks({buf!r})  (an empty chunk is just a 0 length byte)")
    for cut in [b"\x05abc", buf + b"\x04xy"]:
        try:
            tasks.split_chunks(cut)
        except ValueError:
            continue
        raise AssertionError(f"split_chunks({cut!r}) should raise ValueError. The last chunk says it has more bytes than are left.")

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
