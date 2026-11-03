#!/usr/bin/env python3
"""Run with ./check. Tests each task in report.py and lists what still fails."""
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

report = load("report")
rng = random.Random(9)
NAMES = ["alpha", "bravo", "delta", "echo", "kilo"]

def make_readings():
    rows = [(rng.choice(NAMES), rng.randint(0, 40)) for _ in range(12)]
    best = {}
    for n, s in rows:
        best[n] = max(best.get(n, s), s)
    return [f"{n},{s}" for n, s in rows], best

def run_in(work):
    r = subprocess.run([sys.executable, os.path.abspath("report.py"), "data.txt"], cwd=work,
                       capture_output=True, text=True, timeout=10)
    err = (r.stderr.strip().splitlines() or [""])[-1]
    assert r.returncode == 0, f"python3 report.py data.txt stopped with an error ({err}). Try python3 report.py readings.txt yourself."

@task("1 parse_reading")
def _():
    same(report.parse_reading("tower,12"), ["tower", 12], "parse_reading('tower,12')")
    n, s = rng.choice(NAMES), rng.randint(0, 40)
    same(report.parse_reading(f"{n},{s}"), [n, s], f"parse_reading('{n},{s}')")
    try:
        report.parse_reading("no comma here")
    except ValueError:
        pass
    else:
        raise AssertionError("parse_reading('no comma here') should raise ValueError, but it did not")

@task("2 best_snr")
def _():
    same(report.best_snr(["tower,12", "beacon,4", "tower,15", "beacon,2"]), {"tower": 15, "beacon": 4},
         "best_snr(['tower,12', 'beacon,4', 'tower,15', 'beacon,2'])")
    lines, best = make_readings()
    same(report.best_snr(lines), best, f"best_snr({lines})")

@task("3 report_lines")
def _():
    same(report.report_lines({"tower": 15, "beacon": 4}), ["beacon: 4", "tower: 15"], "report_lines({'tower': 15, 'beacon': 4})")
    _, best = make_readings()
    same(report.report_lines(best), [f"{k}: {best[k]}" for k in sorted(best)], f"report_lines({best})")

@task("4 main writes report.txt")
def _():
    lines, best = make_readings()
    work = tempfile.mkdtemp()
    with open(os.path.join(work, "data.txt"), "w") as f:
        f.write("# station,snr\n" + "\n".join(lines[:6]) + "\n\n" + "\n".join(lines[6:]) + "\n")
    here = os.getcwd()
    os.chdir(work)
    try:
        report.main("data.txt")
    finally:
        os.chdir(here)
    out = os.path.join(work, "report.txt")
    assert os.path.exists(out), "main did not create report.txt. It should end with write_lines(\"report.txt\", ...)"
    want = "".join(f"{k}: {best[k]}\n" for k in sorted(best))
    got = open(out).read()
    assert got == want, f"report.txt holds {got!r}, but it should hold {want!r}"

@task("5 python3 report.py FILE works")
def _():
    src = open("report.py").read()
    assert "__main__" in src, "add  if __name__ == \"__main__\":  with main(sys.argv[1]) inside, at the bottom of report.py"
    lines, best = make_readings()
    work = tempfile.mkdtemp()
    with open(os.path.join(work, "data.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")
    run_in(work)
    out = os.path.join(work, "report.txt")
    assert os.path.exists(out), "python3 report.py data.txt did not create report.txt. Does the __main__ block call main(sys.argv[1])?"
    want = "".join(f"{k}: {best[k]}\n" for k in sorted(best))
    assert open(out).read() == want, "The command line made a report.txt that is not the same as what main should write"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
