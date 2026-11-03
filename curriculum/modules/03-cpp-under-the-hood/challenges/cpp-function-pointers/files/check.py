#!/usr/bin/env python3
"""Run with ./check. Tests each task in funcs.cpp and funcs.hpp and lists what still fails."""
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

SRC = "funcs.cpp"
SOURCES = ['funcs.cpp']
TESTS = r"""#include <cstdlib>
#include <iostream>
#include <vector>
#include "funcs.hpp"
static int sub(int a, int b) { return a - b; }
struct seen_log { std::vector<int> seen; };
static void remember(int value, void* context)
{
    static_cast<seen_log*>(context)->seen.push_back(value);
}
static void show(bool ok, uint16_t v) { std::cout << (ok ? "true " : "false ") << (ok ? unsigned(v) : 0u) << "\n"; }
int main(int argc, char** argv)
{
    int t = argc > 1 ? std::atoi(argv[1]) : 0;
    if (t == 2) {
        std::cout << apply(add, 2, 3) << " " << apply(mul, -4, 6) << " " << apply(sub, 10, 4) << "\n";
    } else if (t == 3) {
        int_op p = pick_op('+'), m = pick_op('*');
        std::cout << (p == add) << " " << (m == mul) << " " << (pick_op('?') == nullptr) << " " << (pick_op('-') == nullptr) << "\n";
        if (p && m) std::cout << p(20, 22) << " " << m(6, 7) << "\n";
    } else if (t == 4) {
        std::vector<int> v = {5, -3, 99, 0, 7};
        seen_log l;
        visit_all(v.data(), 5, remember, &l);
        std::cout << l.seen.size() << ":";
        for (int x : l.seen) std::cout << " " << x;
        std::cout << "\n";
        seen_log e;
        visit_all(v.data(), 0, remember, &e);
        std::cout << e.seen.size() << "\n";
    } else if (t == 5) {
        stats s{0, 0};
        update_stats(10, &s); update_stats(-4, &s); update_stats(1000, &s);
        std::cout << s.count << " " << s.sum << "\n";
        stats* heap = new stats{5, 100};
        update_stats(-100, heap);
        std::cout << heap->count << " " << heap->sum << "\n";
        delete heap;
    } else if (t == 6) {
        std::cout << bytes_left(10, 3) << " " << bytes_left(10, 10) << " " << bytes_left(3, 10) << " "
                  << bytes_left(0, 0) << " " << bytes_left(5, SIZE_MAX) << "\n";
        std::cout << (bytes_left(SIZE_MAX, 1) == SIZE_MAX - 1) << "\n";
    } else if (t == 7) {
        std::vector<uint8_t> b = {0x12, 0x34, 0xbe, 0xef, 0x01};   // exactly 5 bytes, so reading b[5] is caught
        uint16_t v = 0;
        bool ok;
        ok = read_be16_at(b.data(), 5, 0, &v); show(ok, v);
        ok = read_be16_at(b.data(), 5, 2, &v); show(ok, v);
        ok = read_be16_at(b.data(), 5, 3, &v); show(ok, v);
        ok = read_be16_at(b.data(), 5, 4, &v); show(ok, v);
        ok = read_be16_at(b.data(), 5, 5, &v); show(ok, v);
        ok = read_be16_at(b.data(), 5, SIZE_MAX, &v); show(ok, v);
        ok = read_be16_at(b.data(), 5, SIZE_MAX - 1, &v); show(ok, v);
        ok = read_be16_at(nullptr, 5, 0, &v); show(ok, v);
        ok = read_be16_at(b.data(), 5, 0, nullptr); show(ok, v);
    }
    return 0;
}
"""

@task("1 type alias byte")
def _():
    started(1, "funcs.hpp")
    exe = build('#include <iostream>\n#include "funcs.hpp"\nint main()\n{\n    byte b = 255;\n    b++;\n    std::cout << static_cast<int>(b) << " " << sizeof(byte) << "\\n";\n    return 0;\n}\n', [])
    same(run_test(exe, 1), ["0 1"], "a byte holding 255, plus 1, and sizeof(byte) (a uint8_t wraps to 0 and is 1 byte)")

@task("2 call through a function pointer")
def _():
    same(test(2), ["5 -24 6"], "apply(add, 2, 3), apply(mul, -4, 6), apply(sub, 10, 4)")

@task("3 return a function pointer")
def _():
    out = test(3)
    same(out[:1], ["1 1 1 1"], "pick_op('+') == add, pick_op('*') == mul, pick_op('?') == nullptr, pick_op('-') == nullptr (1 means yes)")
    same(out[1:], ["42 42"], "calling pick_op('+')(20, 22) and pick_op('*')(6, 7)")

@task("4 callback with context")
def _():
    same(test(4), ["5: 5 -3 99 0 7", "0"], "values the visitor saw for {5, -3, 99, 0, 7}, then the call count for count 0")

@task("5 cast the void* context")
def _():
    same(test(5), ["3 1006", "6 0"], "stats (count sum) after update_stats(10), (-4), (1000); then {5, 100} after update_stats(-100)")

@task("6 unsigned sizes never wrap")
def _():
    out = test(6)
    same(out[:1], ["7 0 0 0 0"], "bytes_left(10,3) (10,10) (3,10) (0,0) (5,SIZE_MAX)")
    same(out[1:], ["1"], "bytes_left(SIZE_MAX, 1) == SIZE_MAX - 1 (1 means yes)")

@task("7 bounds check before reading")
def _():
    want = ["true 4660", "true 48879", "true 61185", "false 0", "false 0", "false 0", "false 0", "false 0", "false 0"]
    got = test(7)
    what = ["offset 0", "offset 2", "offset 3", "offset 4 (only 1 byte left)", "offset 5 (at the end)",
            "offset SIZE_MAX", "offset SIZE_MAX-1 (offset + 2 wraps around to 0!)", "buf nullptr", "out nullptr"]
    for w, g, label in zip(want, got + ["(nothing)"] * len(want), what):
        assert g == w, f"read_be16_at on a 5-byte buffer 12 34 be ef 01 at {label}: got {g!r}, expected {w!r}"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
