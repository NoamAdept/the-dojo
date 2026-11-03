#!/usr/bin/env python3
"""Run with ./check. Tests each task in records.cpp and lists what still fails."""
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

SRC = "records.cpp"
SOURCES = ['records.cpp']
TESTS = r"""#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include "records.hpp"
struct seen_log { std::vector<std::string> seen; };
static void see(uint8_t type, const uint8_t* payload, std::size_t length, void* context)
{
    std::ostringstream s;
    s << unsigned(type) << " " << length;
    for (std::size_t i = 0; i < length; i++) s << " " << std::hex << std::setw(2) << std::setfill('0') << unsigned(payload[i]);
    static_cast<seen_log*>(context)->seen.push_back(s.str());
}
static void run(const std::vector<uint8_t>& d)   // the vector has exactly d.size() bytes, so reading past the end is caught
{
    seen_log l;
    bool ok = parse_records(d.empty() ? nullptr : d.data(), d.size(), see, &l);
    std::cout << (ok ? "true " : "false ") << l.seen.size() << "\n";
    for (const auto& s : l.seen) std::cout << "  " << s << "\n";
}
int main(int argc, char** argv)
{
    int t = argc > 1 ? std::atoi(argv[1]) : 0;
    if (t == 1) {
        run({1, 2, 9, 8, 4, 0, 7, 3, 0xaa, 0xbb, 0xcc});
        run({});
        run({0x10, 1, 0x42});
    } else if (t == 2) {
        run({2, 4, 1});
        run({1, 1, 5, 9});
        run({3, 2, 0xaa});
        run({1, 0, 2, 255, 1, 2, 3});
    } else if (t == 3) {
        std::vector<uint8_t> a = {1, 2, 9, 8, 4, 0}, bad = {2, 4, 1}, many;
        for (int i = 0; i < 300; i++) { many.push_back(uint8_t(i)); many.push_back(0); }
        std::cout << count_records(a.data(), a.size()) << " " << count_records(nullptr, 0) << " "
                  << count_records(bad.data(), bad.size()) << " " << count_records(many.data(), many.size()) << "\n";
    }
    return 0;
}
"""

@task("1 walk the records")
def _():
    out = test(1)
    same(out[:4], ["true 3", "  1 2 09 08", "  4 0", "  7 3 aa bb cc"], "result, visit count and each record (type length payload) for 01 02 09 08 04 00 07 03 aa bb cc")
    same(out[4:5], ["true 0"], "result and visit count for an empty buffer")
    same(out[5:], ["true 1", "  16 1 42"], "result and record for the single record 10 01 42")

@task("2 refuse truncated input")
def _():
    got = test(2)
    for w, buf in ((["false 0"], "02 04 01 (payload cut short)"),
                   (["false 1", "  1 1 05"], "01 01 05 09 (second header cut short)"),
                   (["false 0"], "03 02 aa (payload cut short)"),
                   (["false 1", "  1 0"], "01 00 02 ff 01 02 03 (second payload cut short)")):
        same(got[:len(w)], w, f"result and visited records for {buf}")
        got = got[len(w):]

@task("3 count with your own visitor")
def _():
    same(test(3), ["2 0 -1 300"], "count_records of 01 02 09 08 04 00, an empty buffer, 02 04 01 (truncated), and 300 empty records")

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
