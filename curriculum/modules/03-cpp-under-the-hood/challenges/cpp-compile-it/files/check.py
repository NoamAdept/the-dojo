#!/usr/bin/env python3
"""Run with ./check. Tests each task in meter.cpp and lists what still fails."""
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

import os, re, subprocess, tempfile

FLAGS = ["-std=c++17", "-Wall", "-Wextra", "-Werror", "-Wno-unused-parameter",
         "-fsanitize=address,undefined", "-fno-sanitize-recover=all", "-g"]
TMP = tempfile.mkdtemp(prefix="cpputh-")
HELP = [
    ("undefined reference", "a function the header promises is missing from your .cpp file. Check the spelling, and do not delete any function."),
    ("expected ';'", "a line is missing its `;` at the end. g++ often names the line AFTER the one that is missing it, so look one line up too."),
    ("was not declared in this scope", "you used a name that was never created. Every variable needs a type the first time it appears (like `double x = 1.5;`), and the spelling must match exactly."),
    ("does not name a type", "you used a type name g++ does not know. Did you add the typedef / using line, and spell it the same way?"),
    ("has no member named", "that struct has no field with this name. Look at the struct in the header for the exact field names."),
    ("meant to use '->'", "this is a pointer to a struct, so use -> instead of . to reach the field."),
    ("base operand of '->' has non-pointer type", "this is a struct, not a pointer, so use . instead of ->."),
    ("invalid conversion from 'void*'", "C++ does not turn a void* into another pointer type by itself. Convert it with static_cast, for example `static_cast<stats*>(context)`."),
    ("unused variable", "you created a variable but never used it. Use it, or delete the line."),
    ("no return statement", "this function must return a value on every path."),
    ("control reaches end of non-void function", "this function must return a value on every path."),
    ("comparison of integer expressions of different signedness", "you compared a signed int with an unsigned number. Use std::size_t (or another unsigned type) for both."),
    ("cannot convert", "the types do not match. Check the function and pointer types in the header."),
    ("expected", "something is missing just before the spot g++ points at: often a `;`, a `)` or a `}`."),
]


def explain(err):
    err = err.replace(TMP + "/", "").replace("‘", "'").replace("’", "'")
    err = re.sub(r"(?m)^\./", "", err)
    lines = err.splitlines()
    pick = ([l for l in lines if "undefined reference" in l] or [l for l in lines if ": error:" in l]
            or [l for l in lines if l.strip()] or ["(no message)"])
    first = pick[0].strip()
    plain = next((p for key, p in HELP if key in first),
                 "go to the file:line:column at the start of the message and look closely at that spot.")
    return f"does not compile yet.\n      g++ says: {first}\n      In plain words: {plain}"


def started(n, path=None):
    if f"TODO task {n}" in open(path or SRC).read():
        raise NotImplementedError


_EXE = []


def build(test_src, sources):
    test = os.path.join(TMP, f"test{len(os.listdir(TMP))}.cpp")
    with open(test, "w") as f:
        f.write(test_src)
    exe = test[:-4]
    r = subprocess.run(["g++", *FLAGS, "-I.", *sources, test, "-o", exe], capture_output=True, text=True)
    if r.returncode:
        raise AssertionError("your code " + explain(r.stderr))
    return exe


def run_test(exe, n):
    try:
        r = subprocess.run([exe, str(n)], capture_output=True, text=True, timeout=10,
                           env={**os.environ, "ASAN_OPTIONS": "detect_leaks=0"})
    except subprocess.TimeoutExpired:
        raise AssertionError("the test did not finish within 10 seconds. Is there a loop that never stops?")
    if r.returncode:
        err = r.stderr.replace(TMP + "/", "").replace(os.getcwd() + "/", "")
        why = [l.strip() for l in err.splitlines() if "runtime error" in l]
        if not why:  # AddressSanitizer: say what went wrong and the first line of the learner's file involved
            kind = [l.split("ERROR: AddressSanitizer: ")[1].split(" on ")[0] for l in err.splitlines() if "ERROR: AddressSanitizer" in l]
            where = [l.split(" in ", 1)[1].strip() for l in err.splitlines() if " in " in l and SRC + ":" in l]
            why = [" ".join(kind[:1] + (["in " + where[0]] if where else []))] if kind else [err.strip()[:300]]
        raise AssertionError("the test program crashed: " + why[0]
                             + "\n      In plain words: your code read or wrote memory it should not (for example past the end of a buffer, or through a nullptr), or shifted a number too far.")
    return r.stdout.splitlines()


def test(n):
    """Run hidden test number n against the learner's file and return its output lines."""
    started(n)
    if not _EXE:
        _EXE.append(build(TESTS, SOURCES))
    return run_test(_EXE[0], n)


def same(got, want, what):
    assert got == want, f"{what}: got {got}, expected {want}"

SRC = "meter.cpp"
SOURCES = []
TESTS = r"""#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <string>
#define main meter_main
#include "meter.cpp"
#undef main
int main(int argc, char** argv)
{
    int t = argc > 1 ? std::atoi(argv[1]) : 0;
    if (t == 2) {
        std::cout << average(1, 2, 6) << " " << average(10, 20, 30) << " " << average(0, 0, 9) << " " << average(-3, 4.5, 1.5) << "\n";
    } else if (t == 3) {
        print_average(20);
        print_average(7.0 / 3);
        print_average(100.0 / 7);
        meter_main();
    }
    return 0;
}
"""

@task("1 build clean with strict warnings")
def _():
    r = subprocess.run(["g++", "-std=c++17", "-Wall", "-Wextra", "-Werror", "meter.cpp", "-o", "meter"],
                       capture_output=True, text=True)
    assert r.returncode == 0, "meter.cpp " + explain(r.stderr)

@task("2 operator order")
def _():
    same(test(2), ["3 20 3 1"], "average(1, 2, 6), average(10, 20, 30), average(0, 0, 9), average(-3, 4.5, 1.5) (brackets first, then divide)")

@task("3 one digit after the point")
def _():
    out = test(3)
    same(out[:3], ["average=20.0", "average=2.3", "average=14.3"], "print_average(20), print_average(7.0 / 3), print_average(100.0 / 7) printed (use std::fixed and std::setprecision(1))")
    same(out[3:], ["average=20.0"], "the whole program printed")

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
