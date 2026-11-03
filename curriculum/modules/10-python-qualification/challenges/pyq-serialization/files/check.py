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

import dataclasses, json, os, pickle, tempfile, tasks

D = tempfile.mkdtemp()

@task("1 Item dataclass")
def _():
    assert dataclasses.is_dataclass(tasks.Item) and tasks.Item("ant", 9.5).price == 9.5

@task("2 student_json")
def _():
    assert json.loads(tasks.student_json()) == {"name": "John", "grades": [80, 90]}

@task("3 pickle_roundtrip")
def _():
    data, back = tasks.pickle_roundtrip(True)
    assert isinstance(data, bytes) and back is True

@task("4 frozen Settings")
def _():
    s = tasks.Settings(debug=False)
    try:
        s.debug = True
    except dataclasses.FrozenInstanceError:
        pass
    else:
        raise AssertionError("Settings must be frozen")

@task("5 save/load config")
def _():
    p = os.path.join(D, "cfg.json")
    tasks.save_config({"freq": 100.1e6, "mode": "fm"}, p)
    assert json.load(open(p))["mode"] == "fm" and tasks.load_config(p) == {"freq": 100.1e6, "mode": "fm"}

@task("6 users round trip")
def _():
    p = os.path.join(D, "users.json")
    users = [tasks.User("ann", 31), tasks.User("bo", 22)]
    tasks.serialize_users(users, p)
    assert json.load(open(p)) == [{"name": "ann", "age": 31}, {"name": "bo", "age": 22}]
    assert tasks.deserialize_users(p) == users

@task("7 file_cache")
def _():
    p = os.path.join(D, "cache.pkl")
    calls = []
    def slow(x):
        calls.append(x)
        return x * x
    f = tasks.file_cache(p)(slow)
    assert f(4) == 16 and f(4) == 16 and calls == [4]
    g = tasks.file_cache(p)(slow)  # a fresh wrapper must read the file
    assert g(4) == 16 and calls == [4] and pickle.load(open(p, "rb")) == {4: 16}

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
