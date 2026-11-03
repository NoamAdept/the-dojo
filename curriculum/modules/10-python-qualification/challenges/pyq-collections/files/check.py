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

import collections, tasks

@task("1 multiples of three")
def _():
    assert tasks.multiples_of_three() == [0, 3, 6, 9, 12, 15, 18]

@task("2 invert")
def _():
    assert tasks.invert({"a": 1, "b": 2, "c": 3}) == {1: "a", 2: "b", 3: "c"}

@task("3 Counter")
def _():
    c = tasks.word_counts("the quick brown fox jumps over the lazy dog")
    assert isinstance(c, collections.Counter) and c["the"] == 2 and c["fox"] == 1

@task("4 defaultdict")
def _():
    g = tasks.group_pairs([("A", 1), ("B", 2), ("A", 3)])
    assert isinstance(g, collections.defaultdict) and g == {"A": [1, 3], "B": [2]}

@task("5 student grades")
def _():
    names, grades = tasks.names_and_map([("Alice", 85), ("Bob", 90), ("Charlie", 78)])
    assert names == ["Alice", "Bob", "Charlie"] and grades["Bob"] == 90

@task("6 analyze_text")
def _():
    r = tasks.analyze_text("The Pi! The radio, the antenna.")
    assert r == {"total_words": 6, "unique_words": 4, "most_common_word": ("the", 3)}, r

@task("7 MovingAverage")
def _():
    m = tasks.MovingAverage(3)
    assert [m.add(v) for v in (3, 6, 9, 12)] == [3, 4.5, 6, 9]
    dq = [v for v in vars(m).values() if isinstance(v, collections.deque)]
    assert dq and dq[0].maxlen == 3, "store values in deque(maxlen=n)"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
