#!/usr/bin/env python3
"""Run with ./check. Tests each task in greet.cpp and add.cpp and lists what still fails."""
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

FLAGS = ["-std=c++17", "-Wall", "-Wextra", "-Werror", "-Wno-unused-parameter"]
TMP = tempfile.mkdtemp(prefix="cppfirst-")
HELP = [
    ("undefined reference", "./check looked for a function with this name in your file. It did not find it. Check the spelling. Make sure that you wrote the whole function, and not only a call to it."),
    ("expected ';'", "a line has no semicolon `;` at the end. g++ often shows the line AFTER the line with the problem. So look at the line above it too."),
    ("is not a member of 'std'", "the name after `std::` is not in the standard library. Check the spelling (cout, not cuot). Also check the #include lines at the top (std::cout needs #include <iostream>, std::setprecision needs #include <iomanip>, std::stoi needs #include <string>)."),
    ("was not declared in this scope", "you used a name that C++ does not know. Check the spelling. Create a variable before you use it (like `int count = 0;`). Write your own functions above the place where you use them."),
    ("at end of input", "a `{` has no matching `}`. Every opening brace needs a closing brace."),
    ("unused variable", "you created a variable, but you never used it. Use it, or delete the line."),
    ("no return statement", "this function must give back a value. But it can get to its last `}` without a `return` line."),
    ("control reaches end of non-void function", "this function must give back a value. But it can get to its last `}` without a `return` line."),
    ("suggest parentheses around assignment", "you wrote `=` (store a value) where you probably meant `==` (compare two values)."),
    ("different signedness", "you compared a whole number that can be negative with a whole number that cannot be negative. Use `int` for both."),
    ("missing terminating", "a piece of text is missing its closing quote mark."),
    ("does not guard", "an if, for or while without braces controls only ONE line. Put `{` and `}` around all the lines that belong to it."),
    ("misleading-indentation", "an if, for or while without braces controls only ONE line. Put `{` and `}` around all the lines that belong to it."),
    ("too few arguments", "you called a function with fewer values than it needs."),
    ("too many arguments", "you called a function with more values than it needs."),
    ("no match for 'operator", "a `<<` or `>>` is used on something that cannot be printed in this way. Check that you wrote `std::cout <<` (two `<` signs) and not `<` or `>>`."),
    ("expected ')'", "a `(` has no matching `)`."),
    ("expected '}'", "a `{` has no matching `}`."),
    ("expected", "something is missing just before the place that g++ shows. Often it is a `;`, a `)` or a `}`."),
]


def explain(err):
    err = re.sub(r"\S*/(?=[\w.]+\.cpp:)", "", err).replace(TMP + "/", "").replace("\u2018", "'").replace("\u2019", "'")
    lines = err.splitlines()
    pick = ([l for l in lines if "undefined reference" in l] or [l for l in lines if ": error:" in l]
            or [l for l in lines if l.strip()] or ["(no message)"])
    first = pick[0].strip()
    plain = next((p for key, p in HELP if key in first),
                 "look at the file:line:column at the start of the message. Then look carefully at that place in your file.")
    return f"does not compile yet.\n      g++ says: {first}\n      In plain words: {plain}"


def gxx(args, what):
    r = subprocess.run(["g++", *FLAGS, *args], capture_output=True, text=True)
    if r.returncode:
        raise AssertionError(f"{what} " + explain(r.stderr))


def run(exe, args=(), stdin=""):
    try:
        r = subprocess.run([exe, *map(str, args)], capture_output=True, text=True, timeout=5, input=stdin)
    except subprocess.TimeoutExpired:
        raise AssertionError("the program did not finish in 5 seconds. Is there a loop that never stops?")
    if r.returncode < 0:
        raise AssertionError(f"the program crashed (signal {-r.returncode}). Maybe it used a word from argv that the user did not type (check argc first). Or maybe it called std::stoi on a word that is not a number, without try/catch.")
    return r


def program(src):
    """Compile a whole program (with its own main) and return the executable's path."""
    exe = os.path.join(TMP, src[:-4])
    gxx([src, "-o", exe], src)
    return exe


def calls(header, body, src="tasks.cpp"):
    """Compile the learner's file (its main renamed) with a small test main; return its output."""
    obj = os.path.join(TMP, "learner.o")
    gxx(["-Dmain=learner_main", "-I.", "-c", src, "-o", obj], src)
    test = os.path.join(TMP, "test.cpp")
    with open(test, "w") as f:
        f.write("#include <iostream>\n#include <iomanip>\n" + header + "\nint main()\n{\n" + body + "\n    return 0;\n}\n")
    exe = os.path.join(TMP, "test")
    gxx(["-I.", test, obj, "-o", exe], "the test program")
    return run(exe).stdout


def shown(kind, v):
    if kind == "double":
        return f"{v:.3f}"
    if kind == "bool":
        return "true" if v else "false"
    return str(v)


def check_values(header, cases, kind="int", src="tasks.cpp"):
    """cases: list of (C++ expression, expected value). Calls each and compares the printed result."""
    setup = {"double": "    std::cout << std::fixed << std::setprecision(3);\n",
             "bool": "    std::cout << std::boolalpha;\n"}.get(kind, "")
    body = setup + "".join(f"    std::cout << ({e}) << '\\n';\n" for e, _ in cases)
    got = calls(header, body, src).splitlines()
    for (e, want), g in zip(cases, got + ["(nothing)"] * len(cases)):
        want = shown(kind, want)
        assert g == want, f"{e} gave {g}, expected {want}"


def with_values(src, swaps):
    """Swap the given starting values in src for others, compile, run, return output lines."""
    text = open(src).read()
    for old, new in swaps:
        # Spacing may differ (an editor can reformat `int x = 7;` as `int x=7;`); the words may not.
        pattern = r"\s*".join(re.escape(part) for part in re.findall(r"\w+|[^\w\s]", old))
        assert re.search(pattern, text), f"keep the line `{old}` in {src} as it was. ./check puts other values there to test your code."
        text = re.sub(pattern, lambda _m: new, text)
    d = tempfile.mkdtemp(dir=TMP)
    path = os.path.join(d, src)
    with open(path, "w") as f:
        f.write(text)
    gxx([path, "-o", path[:-4]], src)
    return run(path[:-4]).stdout.splitlines()


def need(lines, want, when=""):
    assert want in lines, f"expected a line `{want}`{when}, but the program printed: {lines}"


def go(src, args):
    return run(program(src), args)

@task("1 greet NAME")
def _():
    for name in ["Ada", "Grace", "pi"]:
        r = go("greet.cpp", [name])
        assert r.stdout == f"Hello, {name}!\n", f"./greet {name} printed {r.stdout!r}, expected 'Hello, {name}!' and a new line"
        assert r.returncode == 0, f"./greet {name} exited with status {r.returncode}, expected 0"

@task("2 greet with no name")
def _():
    r = go("greet.cpp", [])
    assert r.stdout.strip() == "usage: ./greet NAME", f"./greet with no name printed {r.stdout!r}, expected 'usage: ./greet NAME'"
    assert r.returncode == 1, f"./greet with no name exited with status {r.returncode}, expected 1 (return 1;)"
    r = go("greet.cpp", ["Linus", "Torvalds"])
    assert r.stdout == "Hello, Linus!\n", f"./greet Linus Torvalds printed {r.stdout!r}, expected only 'Hello, Linus!'"

@task("3 add two numbers")
def _():
    for a, b in [(3, 4), (-10, 4), (0, 0), (1200, 34)]:
        out = go("add.cpp", [a, b]).stdout.strip()
        assert out == str(a + b), f"./add {a} {b} printed {out!r}, expected {a + b}"

@task("4 add any count")
def _():
    for nums in [[1, 2, 3, 4], [], [42], [5, -5, 10, 20, -1, 7, 100]]:
        out = go("add.cpp", nums).stdout.strip()
        shown = " ".join(map(str, nums))
        assert out == str(sum(nums)), f"./add {shown} printed {out!r}, expected {sum(nums)}"

@task("5 add refuses words that are not numbers")
def _():
    for args, bad in [(["3", "abc"], "abc"), (["hello"], "hello"), (["1", "2", "x9", "4"], "x9")]:
        r = go("add.cpp", args)
        shown = " ".join(args)
        assert r.stdout.strip() == f"not a number: {bad}", f"./add {shown} printed {r.stdout!r}, expected 'not a number: {bad}'"
        assert r.returncode == 1, f"./add {shown} exited with status {r.returncode}, expected 1 (return 1;)"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
