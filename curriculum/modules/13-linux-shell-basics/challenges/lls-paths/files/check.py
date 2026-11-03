#!/usr/bin/env python3
"""Run with ./check. Tests each task in answers/task1.sh to answers/task8.sh and lists what still fails."""
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

import os, pathlib, shutil, subprocess, tempfile

HERE = pathlib.Path(".").resolve()

def answer(n):
    """Path of answers/taskN.sh; NotImplementedError while it still says TODO."""
    p = HERE / "answers" / f"task{n}.sh"
    if not p.exists() or "TODO" in p.read_text():
        raise NotImplementedError
    return p

def sandbox(files=None):
    """Fresh temp dir filled with {relative path: text or bytes}. Returns its Path."""
    # ponytail: sandboxes live in /tmp and are left for the OS to clean.
    d = pathlib.Path(tempfile.mkdtemp(prefix="academy-sh-"))
    for rel, data in (files or {}).items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data) if isinstance(data, bytes) else p.write_text(data)
    return d

def run(n, cwd=None, stdin=None, env=None, args=(), timeout=20):
    """Run answers/taskN.sh with bash in cwd (a new sandbox by default).
    Returns (CompletedProcess, cwd). HOME points at the sandbox unless env overrides it."""
    cwd = cwd or sandbox()
    e = {**os.environ, "HOME": str(cwd), **(env or {})}
    r = subprocess.run(["bash", str(answer(n)), *args], cwd=cwd, input=stdin, env=e,
                       capture_output=True, text=True, timeout=timeout)
    return r, cwd

import random, re
RNG = random.Random(102)


def word(n=8):
    return "".join(RNG.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(n))


def secret(tag="s"):
    return "academy{%s_%s}" % (tag, word(12))


def dojo(tree=None, subs=None):
    """Fresh fake root from TREE and PROGS (plus overrides). Returns its resolved Path."""
    root = sandbox({**TREE, **(tree or {})}).resolve()
    for d in ("home/hacker", "tmp"):
        (root / d).mkdir(parents=True, exist_ok=True)
    allsubs = {**PRACTICE, **(subs or {})}
    for rel, body in PROGS.items():
        for k, v in allsubs.items():
            body = body.replace(k, v)
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body)
        p.chmod(0o755)
    return root


def go(n, root, cwd=None, stdin=None, env=None, timeout=20):
    """Run answers/taskN.sh the way the README describes. Returns (result, token)."""
    home = root / "home/hacker"
    tok = word()
    e = {"DOJO": str(root), "HOME": str(home), "TOKEN": tok,
         "PATH": str(root / "bin") + os.pathsep + os.environ.get("PATH", ""), **(env or {})}
    r, _ = run(n, cwd=cwd or home, stdin=stdin, env=e, timeout=timeout)
    return r, tok


def show(r):
    return f"(stdout: {r.stdout[-300:]!r}, stderr: {r.stderr[-300:]!r})"


def reports(r, tok):
    """Each run of a reporting program whose token matches: dict(argv0, cwd, args)."""
    out, cur = [], None
    for line in r.stdout.splitlines():
        if line.startswith("RAN argv0="):
            cur = {"argv0": line[10:], "args": []}
        elif cur is not None and line.startswith("RAN cwd="):
            cur["cwd"] = line[8:]
        elif cur is not None and line.startswith("RAN arg="):
            cur["args"].append(line[8:])
        elif cur is not None and line.startswith("RAN token="):
            if line[10:] == tok:
                out.append(cur)
            cur = None
    return out


def report(r, tok, prog="the challenge program"):
    reps = reports(r, tok)
    assert reps, f"{prog} never ran {show(r)}"
    return reps[-1]


# --- shellwords: begin (copy of platform/academy/shellwords.py) ---
_SH_OPS = ("&&", "||", ";;", "|&", ";", "|", "&", "(", ")")
_SH_REDIRS = ("&>>", "<<<", "<<-", "<<", ">>", ">&", "<&", "&>", ">|", "<>", ">", "<")
_SH_KEYWORDS = {"if", "then", "else", "elif", "fi", "do", "done", "while", "until", "time", "!", "{", "}"}
_SH_WRAPPERS = {"command", "exec", "nohup", "env", "builtin"}
_SH_SKIP = {"for", "case", "esac", "select", "function", "[[", "]]"}


def _sh_close(text, i, opener="(", closer=")"):
    """Index just after the bracket that closes the one opened before text[i]."""
    depth, q = 1, None
    while i < len(text):
        c = text[i]
        if q:
            if c == "\\" and q == '"':
                i += 1
            elif c == q:
                q = None
        elif c in "'\"":
            q = c
        elif c == "\\":
            i += 1
        elif c == opener:
            depth += 1
        elif c == closer:
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return len(text) + 1  # never closed: as if a ) followed the end


def _sh_tokens(text):
    """Words, operators and redirections of text. Commands inside $(...), `...`, <(...) and
    >(...) become ("sub", commands) tokens; the word that holds them keeps them as typed."""
    toks, val, raw, have = [], [], [], False
    i, n = 0, len(text)

    def flush():
        nonlocal val, raw, have
        if have:
            toks.append(("w", "".join(val), "".join(raw)))
        val, raw, have = [], [], False

    def nested(inner):
        toks.append(("sub", shell_commands(inner), inner))

    while i < n:
        c = text[i]
        if c == "\n":
            flush()
            toks.append(("op", "\n", "\n"))
            i += 1
        elif c in " \t":
            flush()
            i += 1
        elif c == "#" and not have:
            while i < n and text[i] != "\n":
                i += 1
        elif c == "\\":
            if text[i + 1:i + 2] == "\n":
                i += 2
                continue
            val.append(text[i + 1:i + 2])
            raw.append(text[i:i + 2])
            have, i = True, i + 2
        elif c == "'":
            j = text.find("'", i + 1)
            j = n if j < 0 else j
            val.append(text[i + 1:j])
            raw.append(text[i:j + 1])
            have, i = True, j + 1
        elif c == '"':
            j = i + 1
            while j < n and text[j] != '"':
                if text[j] == "\\" and text[j + 1:j + 2] in ('"', "\\", "$", "`", "\n"):
                    val.append(text[j + 1])
                    j += 2
                    continue
                if text.startswith("$(", j) and not text.startswith("$((", j):
                    k = _sh_close(text, j + 2)
                    nested(text[j + 2:k - 1])
                    val.append(text[j:k])
                    j = k
                    continue
                val.append(text[j])
                j += 1
            raw.append(text[i:j + 1])
            have, i = True, j + 1
        elif text.startswith("$((", i):
            k = _sh_close(text, i + 3)
            k = k + 1 if text[k:k + 1] == ")" else k
            val.append(text[i:k])
            raw.append(text[i:k])
            have, i = True, k
        elif text.startswith("$(", i) or (not have and text[i:i + 2] in ("<(", ">(")):
            k = _sh_close(text, i + 2)
            nested(text[i + 2:k - 1])
            val.append(text[i:k])
            raw.append(text[i:k])
            have, i = True, k
        elif c == "`":
            j = text.find("`", i + 1)
            j = n if j < 0 else j
            nested(text[i + 1:j])
            val.append(text[i:j + 1])
            raw.append(text[i:j + 1])
            have, i = True, j + 1
        else:
            redir = next((r for r in _SH_REDIRS if text.startswith(r, i)), None)
            op = None if redir else next((o for o in _SH_OPS if text.startswith(o, i)), None)
            if redir:
                if have and "".join(raw).isdigit():  # 2>file: the 2 is a file descriptor, not a word
                    val, raw, have = [], [], False
                flush()
                toks.append(("redir", redir, redir))
                i += len(redir)
            elif op:
                flush()
                toks.append(("op", op, op))
                i += len(op)
            else:
                val.append(c)
                raw.append(c)
                have, i = True, i + 1
    flush()
    return toks


def shell_commands(text):
    """Every simple command in a bash script, in order, as a list of words (quotes removed).

    `VAR=value` prefixes, keywords (if, then, do, while, !, time...) and wrappers (command,
    exec, env, nohup) are dropped, and so is every redirection with its target. Commands
    inside $(...), backticks, <(...) and >(...) come out as commands of their own.
    `for`/`case` headers and `[[ ... ]]` tests are not commands and are skipped.
    """
    out = []
    toks = _sh_tokens(_sh_without_heredocs(text))
    cmd, skip_next = [], False

    def end():
        nonlocal cmd
        words = cmd
        while words and (words[0] in _SH_KEYWORDS or words[0] in _SH_WRAPPERS or _sh_is_assignment(words[0])):
            words = words[1:]
        if words and words[0] not in _SH_SKIP:
            out.append(words)
        cmd = []

    for kind, value, _raw in toks:
        if kind == "sub":
            out.extend(value)
        elif kind == "redir":
            skip_next = True
        elif kind == "op":
            skip_next = False
            end()
        elif skip_next:
            skip_next = False
        else:
            cmd.append(value)
    end()
    return out


def _sh_is_assignment(word):
    name, eq, _ = word.partition("=")
    return bool(eq) and name.replace("_", "a").isalnum() and not name[:1].isdigit()


def _sh_without_heredocs(text):
    """text with the bodies of here-documents (<<EOF ... EOF) removed."""
    lines, out, i = text.split("\n"), [], 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        i += 1
        for delim, strip_tabs in _sh_heredoc_delims(line):
            while i < len(lines) and (lines[i].lstrip("\t") if strip_tabs else lines[i]) != delim:
                i += 1
            i += 1
    return "\n".join(out)


def _sh_heredoc_delims(line):
    """(delimiter, strip_tabs) for each unquoted << on the line."""
    found, i, q = [], 0, None
    while i < len(line):
        c = line[i]
        if q:
            q = None if c == q else q
        elif c in "'\"":
            q = c
        elif c == "#" and (i == 0 or line[i - 1] in " \t"):
            break
        elif line.startswith("<<", i) and not line.startswith("<<<", i):
            strip_tabs = line.startswith("<<-", i)
            j = i + 2 + strip_tabs
            while j < len(line) and line[j] in " \t":
                j += 1
            k = j
            while k < len(line) and line[k] not in " \t;&|<>()":
                k += 1
            word = line[j:k].replace('"', "").replace("'", "").replace("\\", "")
            if word:
                found.append((word, strip_tabs))
            i = k
            continue
        elif line.startswith("<<<", i):
            i += 3
            continue
        i += 1
    return found


def invocations(text, prog):
    """Argument lists of every call to prog in the script. prog matches a command typed as
    prog, ./prog, any/path/prog or "$DOJO/.../prog" (the last part of the path counts)."""
    return [words[1:] for words in shell_commands(text) if words[0].rstrip("/").rsplit("/", 1)[-1] == prog]
# --- shellwords: end ---


def script(n):
    """Text of answers/taskN.sh."""
    return answer(n).read_text()


def lines(r):
    return [x for x in r.stdout.splitlines() if x.strip()]

TREE = {'var/lib/academy/.keep': '', 'etc/.keep': '', 'usr/share/.keep': '', 'var/log/.keep': '', 'home/.keep': '', 'tmp/.keep': ''}
PROGS = {'pwn': '#!/bin/bash\necho "(this program reports how you ran it; ./check reads the RAN lines)" >&2\nprintf \'RAN argv0=%s\\n\' "$0"\nprintf \'RAN cwd=%s\\n\' "$(pwd -P)"\nfor a in "$@"; do printf \'RAN arg=%s\\n\' "$a"; done\nprintf \'RAN token=%s\\n\' "${TOKEN:-practice}"\n', 'challenge/run': '#!/bin/bash\necho "(this program reports how you ran it; ./check reads the RAN lines)" >&2\nprintf \'RAN argv0=%s\\n\' "$0"\nprintf \'RAN cwd=%s\\n\' "$(pwd -P)"\nfor a in "$@"; do printf \'RAN arg=%s\\n\' "$a"; done\nprintf \'RAN token=%s\\n\' "${TOKEN:-practice}"\n', 'challenge/position': '#!/bin/bash\necho "(this program reports how you ran it; ./check reads the RAN lines)" >&2\nprintf \'RAN argv0=%s\\n\' "$0"\nprintf \'RAN cwd=%s\\n\' "$(pwd -P)"\nfor a in "$@"; do printf \'RAN arg=%s\\n\' "$a"; done\nprintf \'RAN token=%s\\n\' "${TOKEN:-practice}"\n', 'challenge/tour': '#!/bin/bash\necho "(this program reports how you ran it; ./check reads the RAN lines)" >&2\nprintf \'RAN argv0=%s\\n\' "$0"\nprintf \'RAN cwd=%s\\n\' "$(pwd -P)"\nfor a in "$@"; do printf \'RAN arg=%s\\n\' "$a"; done\nprintf \'RAN token=%s\\n\' "${TOKEN:-practice}"\n', 'challenge/copyflag': '#!/bin/bash\ncase "$1" in\n    /*) ;;\n    *) echo "copyflag: give me an ABSOLUTE path (it must start with /), got: \'$1\'" >&2; exit 1;;\nesac\ncase "$1" in\n    "$HOME"/*) ;;\n    *) echo "copyflag: the path must be inside your home directory ($HOME)" >&2; exit 1;;\nesac\necho "@SECRET@" > "$1" && echo "copied the secret to $1"\n'}
PRACTICE = {'@SECRET@': 'academy{practice_home}'}


TOUR = ['etc', 'usr/share', 'var/log', 'home', 'tmp']

@task("1 the root: absolute path")
def _():
    root = dojo()
    r, tok = go(1, root)
    rep = report(r, tok, "$DOJO/pwn")
    assert rep["argv0"].startswith("/"), f"run it by its absolute path. You used {rep['argv0']!r}"
    assert os.path.normpath(rep["argv0"]) == f"{root}/pwn", f"run $DOJO/pwn. You ran {rep['argv0']!r}"

@task("2 program and absolute paths")
def _():
    root = dojo()
    r, tok = go(2, root)
    rep = report(r, tok, "$DOJO/challenge/run")
    assert rep["argv0"].startswith("/") and os.path.normpath(rep["argv0"]) == f"{root}/challenge/run", f"use the absolute path \"$DOJO/challenge/run\". You used {rep['argv0']!r}"

@task("3 position thy self")
def _():
    root = dojo()
    r, tok = go(3, root)
    rep = report(r, tok, "$DOJO/challenge/position")
    want = str(root / "var/lib/academy")
    assert rep["cwd"] == want, f"it ran in {rep['cwd']}, but must run with working directory $DOJO/var/lib/academy"

@task("4 position elsewhere, five times")
def _():
    root = dojo()
    r, tok = go(4, root)
    cwds = [x["cwd"] for x in reports(r, tok) if x["argv0"].endswith("challenge/tour")]
    want = [str(root / d) for d in TOUR]
    assert cwds == want, f"tour ran from {[c.replace(str(root), '$DOJO') for c in cwds]}, expected {['$DOJO/' + d for d in TOUR]}"

@task("5 implicit relative path from the root")
def _():
    root = dojo()
    r, tok = go(5, root)
    rep = report(r, tok, "challenge/run")
    assert rep["cwd"] == str(root), f"cd to \"$DOJO\" first (it ran in {rep['cwd']})"
    assert rep["argv0"] == "challenge/run", f"call it as challenge/run. You used {rep['argv0']!r}"

@task("6 explicit relative path with .")
def _():
    root = dojo()
    r, tok = go(6, root)
    rep = report(r, tok, "challenge/run")
    assert rep["cwd"] == str(root), f"cd to \"$DOJO\" first (it ran in {rep['cwd']})"
    a = rep["argv0"]
    assert not a.startswith("/"), f"use a relative path. You used {a!r}"
    assert "." in a.split("/"), f"put a `.` in the relative path. You used {a!r}"

@task("7 run a program in the current directory")
def _():
    root = dojo()
    r, tok = go(7, root)
    rep = report(r, tok, "run")
    assert rep["cwd"] == str(root / "challenge"), f"cd to \"$DOJO/challenge\" first (it ran in {rep['cwd']})"
    a = rep["argv0"]
    assert a.split("/")[0] == "." and os.path.normpath(a) == "run", f"call it as ./run. You used {a!r}"

@task("8 home sweet home")
def _():
    s = secret("home")
    root = dojo(subs={"@SECRET@": s})
    r, _ = go(8, root)
    home = root / "home/hacker"
    got = [p for p in home.iterdir() if p.is_file() and p.read_text().strip() == s]
    assert got, f"no file in your home directory holds the secret {show(r)}"
    ok = [a for a in invocations(script(8), "copyflag") if a and a[0].startswith("~/") and len(a[0]) <= 3]
    assert ok, "pass copyflag an argument that starts with ~/ and that you type with 3 characters or fewer, like ~/x"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
