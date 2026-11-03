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
rng = random.Random(7)
VOCAB = ["fm", "am", "Pi", "radio", "SIGNAL", "noise", "go"]

@task("1 clean_upper")
def _():
    for text in ["  fm radio\n", "abc", "\t Pi Radio  ", "x"]:
        same(tasks.clean_upper(text), text.strip().upper(), f"clean_upper({text!r})")

@task("2 words")
def _():
    for s in ["the quick fox", "one", "  spaced   out  ", " ".join(rng.choice(VOCAB) for _ in range(6))]:
        same(tasks.words(s), s.split(), f"words({s!r})")

@task("3 dashed")
def _():
    for parts in [["a", "b"], ["solo"], [], ["2026", "10", "06"]]:
        same(tasks.dashed(parts), "-".join(parts), f"dashed({parts})")

@task("4 make_station")
def _():
    for name, freq in [("Pi Radio", 433.92), ("Tower", 145.8)]:
        same(tasks.make_station(name, freq), {"name": name, "freq": freq}, f"make_station({name!r}, {freq})")

@task("5 mode_of")
def _():
    same(tasks.mode_of({"name": "a", "mode": "AM"}), "AM", "mode_of({'name': 'a', 'mode': 'AM'})")
    same(tasks.mode_of({"name": "a"}), "FM", "mode_of({'name': 'a'})")
    same(tasks.mode_of({}), "FM", "mode_of({})")

@task("6 parse_pair")
def _():
    for line in ["gain = 18", "mode= FM", "label = roof=antenna", "  freq=433  "]:
        k, v = line.split("=", 1)
        same(tasks.parse_pair(line), [k.strip(), v.strip()], f"parse_pair({line!r})")

@task("7 count_words")
def _():
    s = " ".join(rng.choice(VOCAB) for _ in range(20))
    for sentence in ["Go go STOP", "a", "", s]:
        want = {}
        for w in sentence.lower().split():
            want[w] = want.get(w, 0) + 1
        same(tasks.count_words(sentence), want, f"count_words({sentence!r})")

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
