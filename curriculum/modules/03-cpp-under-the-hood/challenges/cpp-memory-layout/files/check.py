#!/usr/bin/env python3
"""Run with ./check. Tests each task in layout.cpp and lists what still fails."""
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

SRC = "layout.cpp"
SOURCES = ['layout.cpp']
TESTS = r"""#include <cstdlib>
#include <iostream>
#include <vector>
#include "layout.hpp"
static void show(bool ok, const header& h)
{
    std::cout << ok << " " << h.tag[0] << h.tag[1] << " " << unsigned(h.flags) << " " << unsigned(h.length) << "\n";
}
int main(int argc, char** argv)
{
    int t = argc > 1 ? std::atoi(argv[1]) : 0;
    std::vector<uint8_t> six = {'R', 'X', 0x34, 0x12, 0xa5, 9};   // vectors of exact size: reading past the end is caught
    if (t == 1) {
        std::vector<uint8_t> five = {'R', 'X', 0x34, 0x12, 0xa5};
        header h{};
        h.flags = 77;
        std::cout << decode_header(five.data(), 5, &h) << decode_header(nullptr, 6, &h)
                  << decode_header(six.data(), 6, nullptr) << decode_header(six.data(), 0, &h)
                  << " " << unsigned(h.flags) << "\n";
    } else if (t == 2) {
        header h{};
        bool ok = decode_header(six.data(), 6, &h);
        show(ok, h);
        std::vector<uint8_t> go = {'G', 'O', 0, 0, 0, 0xff};
        ok = decode_header(go.data(), 6, &h);
        show(ok, h);
    } else if (t == 3) {
        std::vector<std::vector<uint8_t>> cases = {six, {'A', 'B', 0xef, 0xbe, 0, 0}, {'A', 'B', 1, 0, 0, 0}, {'A', 'B', 0, 1, 0, 0}};
        const char* sep = "";
        for (const auto& c : cases) {
            header h{};
            decode_header(c.data(), c.size(), &h);
            std::cout << sep << h.sequence;
            sep = " ";
        }
        std::cout << "\n";
    }
    return 0;
}
"""

@task("1 refuse bad input")
def _():
    same(test(1), ["0000 77"], "decode_header with only 5 bytes, data nullptr, out nullptr, size 0 (0 means false), then the untouched flags field")

@task("2 copy the single bytes")
def _():
    same(test(2), ["1 RX 165 9", "1 GO 0 255"], "return value, tag, flags and length decoded from 52 58 34 12 a5 09 and 47 4f 00 00 00 ff")

@task("3 little-endian sequence")
def _():
    same(test(3), ["4660 48879 1 256"], "sequence (in decimal) from bytes 2-3 = 34 12, ef be, 01 00, 00 01 (low byte first)")

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
