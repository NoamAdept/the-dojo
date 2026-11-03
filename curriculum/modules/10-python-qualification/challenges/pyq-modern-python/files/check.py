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

import dataclasses, tasks

@task("1 f-string debug")
def _():
    assert tasks.debug_line(10, 20) == "a=10, b=20, a*b=200"

@task("2 walrus drain")
def _():
    w = ["apple", "banana", "cherry", "date"]
    assert tasks.drain(w) == ["date", "cherry", "banana", "apple"] and w == []
    import ast, inspect, textwrap
    tree = ast.parse(textwrap.dedent(inspect.getsource(tasks.drain)))
    assert any(isinstance(n, ast.NamedExpr) for n in ast.walk(tree)), "use the walrus operator (:=) in drain"

@task("3 Product dataclass")
def _():
    assert dataclasses.is_dataclass(tasks.Product)
    p = tasks.Product("SDR", 30.0)
    assert p.in_stock is True and p == tasks.Product("SDR", 30.0, True)

@task("4 dict merge")
def _():
    d = {"gain": 10, "rate": 1}
    assert tasks.merge(d, {"gain": 30}) == {"gain": 30, "rate": 1} and d == {"gain": 10, "rate": 1}

@task("5 describe_shape")
def _():
    assert tasks.describe_shape(("circle", 5)) == "circle r=5"
    assert tasks.describe_shape(("rect", 10, 20)) == "rect 10x20"
    assert tasks.describe_shape(("blob",)) == "unknown"

@task("6 load_config")
def _():
    assert tasks.load_config("a/b.json") == {"format": "json", "version": 1}
    assert tasks.load_config("notes.txt") == {"format": "text", "lines": 0}
    try:
        tasks.load_config("x.yaml")
    except ValueError:
        pass
    else:
        raise AssertionError(".yaml should raise ValueError")

@task("7 parse_packet")
def _():
    c = tasks.parse_packet(("CONNECT", "127.0.0.1", 8080))
    assert type(c).__name__ == "ConnectPacket" and dataclasses.is_dataclass(c) and c.port == 8080
    d = tasks.parse_packet(("DATA", 7, b"iq"))
    assert type(d).__name__ == "DataPacket" and d.payload == b"iq"
    assert type(tasks.parse_packet(("DISCONNECT", 7))).__name__ == "DisconnectPacket"
    for bad in [("CONNECT", "x", "80"), ("PING",), "junk"]:
        try:
            tasks.parse_packet(bad)
        except ValueError:
            continue
        raise AssertionError(f"{bad!r} should raise ValueError")

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
