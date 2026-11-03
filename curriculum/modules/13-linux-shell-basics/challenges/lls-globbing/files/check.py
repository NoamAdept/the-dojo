#!/usr/bin/env python3
"""Run with ./check. Tests each task in answers/task1.sh to answers/task10.sh and lists what still fails."""
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
RNG = random.Random(105)


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

TREE = {'challenge/files/file_a': '', 'challenge/files/file_b': '', 'challenge/files/file_c': '', 'challenge/files/file_d': '', 'challenge/files/file_e': '', 'challenge/files/file_f': '', 'challenge/files/file_g': '', 'challenge/files/file_h': '', 'challenge/files/file_i': '', 'challenge/files/file_j': '', 'challenge/files/file_k': '', 'challenge/files/file_l': '', 'challenge/files/file_m': '', 'challenge/files/file_n': '', 'challenge/files/file_o': '', 'challenge/files/file_p': '', 'challenge/files/file_q': '', 'challenge/files/file_r': '', 'challenge/files/file_s': '', 'challenge/files/file_t': '', 'challenge/files/file_u': '', 'challenge/files/file_v': '', 'challenge/files/file_w': '', 'challenge/files/file_x': '', 'challenge/files/file_y': '', 'challenge/files/file_z': '', 'challenge/words/amazing': '', 'challenge/words/beautiful': '', 'challenge/words/challenging': '', 'challenge/words/delightful': '', 'challenge/words/educational': '', 'challenge/words/fantastic': '', 'challenge/words/great': '', 'challenge/words/happy': '', 'challenge/words/incredible': '', 'challenge/words/jovial': '', 'challenge/words/kind': '', 'challenge/words/laughing': '', 'challenge/words/magical': '', 'challenge/words/nice': '', 'challenge/words/optimistic': '', 'challenge/words/pwning': '', 'challenge/words/queenly': '', 'challenge/words/radiant': '', 'challenge/words/splendid': '', 'challenge/words/thrilling': '', 'challenge/words/uplifting': '', 'challenge/words/victorious': '', 'challenge/words/wonderful': '', 'challenge/words/xenial': '', 'challenge/words/youthful': '', 'challenge/words/zesty': '', 'challenge/tabfiles/hack-the-planet': '', 'challenge/tabfiles/pwn': '', 'challenge/tabfiles/pwn-college': '', 'challenge/tabfiles/pwn-the-planet': '', 'challenge/tabfiles/pwncollege-family': '', 'challenge/tabfiles/pwncollege-flamingo': '', 'challenge/tabfiles/pwncollege-flyswatter': '', 'challenge/tabfiles/pwncollege-hacking': '', 'challenge/pwncollege': 'academy{practice_tab}\n', 'cache/.keep': ''}
PROGS = {'challenge/run': '#!/bin/bash\necho "(this program reports how you ran it; ./check reads the RAN lines)" >&2\nprintf \'RAN argv0=%s\\n\' "$0"\nprintf \'RAN cwd=%s\\n\' "$(pwd -P)"\nfor a in "$@"; do printf \'RAN arg=%s\\n\' "$a"; done\nprintf \'RAN token=%s\\n\' "${TOKEN:-practice}"\n', 'bin/pwncollege-practice': '#!/bin/bash\necho "you found me"\n'}
PRACTICE = {}


WORDS = ['amazing', 'beautiful', 'challenging', 'delightful', 'educational', 'fantastic', 'great', 'happy', 'incredible', 'jovial', 'kind', 'laughing', 'magical', 'nice', 'optimistic', 'pwning', 'queenly', 'radiant', 'splendid', 'thrilling', 'uplifting', 'victorious', 'wonderful', 'xenial', 'youthful', 'zesty']
TABFILES = ['hack-the-planet', 'pwn', 'pwn-college', 'pwn-the-planet', 'pwncollege-family', 'pwncollege-flamingo', 'pwncollege-flyswatter', 'pwncollege-hacking']

DOJO_FORMS = ("$DOJO", "${DOJO}")

def cd_globs(n):
    """Each GLOB the script used to cd into $DOJO: `cd "$DOJO"/GLOB`, or `cd "$DOJO"` then `cd GLOB`."""
    found, at_root = [], False
    for args in invocations(script(n), "cd"):
        a = args[0] if args else ""
        head, _, rest = a.partition("/")
        if head in DOJO_FORMS and rest.strip("/"):
            found.append(rest.rstrip("/"))
        elif at_root and a and not a.startswith(("/", "$", "~", "-")):
            found.append(a.rstrip("/"))
        at_root = head in DOJO_FORMS and not rest.strip("/")
    return found

def run_args(n):
    found = invocations(script(n), "run")
    assert found, "call \"$DOJO/challenge/run\" in your script"
    return found[-1]

def glob_run(n, cwd_rel, want, check_arg):
    root = dojo()
    r, tok = go(n, root)
    rep = report(r, tok)
    wcwd = str(root / cwd_rel) if cwd_rel else str(root / "home/hacker")
    assert rep["cwd"] == wcwd, f"run it from {cwd_rel and '$DOJO/' + cwd_rel or 'your home directory'} (it ran in {rep['cwd']})"
    args = run_args(n)
    assert len(args) == 1, f"pass exactly 1 argument, and make it a glob. You typed {args}"
    check_arg(args[0])
    want = [w.replace("@ROOT@", str(root)) for w in want]
    assert sorted(rep["args"]) == sorted(want), f"your glob expanded to {[a.replace(str(root), '$DOJO') for a in rep['args']]}"
    return args[0]

def cd_glob(n, rule):
    root = dojo()
    r, tok = go(n, root)
    rep = report(r, tok)
    assert rep["cwd"] == str(root / "challenge"), f"cd into $DOJO/challenge before running it (it ran in {rep['cwd']})"
    globs = cd_globs(n)
    assert globs, 'use cd "$DOJO"/GLOB'
    rule(globs[-1])

@task("1 matching with *")
def _():
    def rule(g):
        assert "*" in g, f"use * in the cd argument after $DOJO/. You typed {g!r}"
        assert len(g) <= 4, f"the part after $DOJO/ must have 4 characters or fewer. Yours is {g!r}"
    cd_glob(1, rule)

@task("2 matching with ?")
def _():
    def rule(g):
        assert "?" in g and "*" not in g, f"use ? and do not use *. You typed {g!r}"
        assert "c" not in g and "l" not in g, f"change every c and l to ?. You typed {g!r}"
    cd_glob(2, rule)

@task("3 matching with []")
def _():
    def rule(a):
        assert "[" in a, f"use a [] glob. You typed {a!r}"
    glob_run(3, "challenge/files", ["file_a", "file_b", "file_h", "file_s"], rule)

@task("4 matching paths with []")
def _():
    def rule(a):
        assert "[" in a, f"use a [] glob. You typed {a!r}"
    glob_run(4, "", [f"@ROOT@/challenge/files/file_{c}" for c in "abhs"], rule)

@task("5 multiple globs")
def _():
    def rule(a):
        assert len(a) <= 3 and a.count("*") == 2, f"use a glob of 3 characters or fewer, with 2 *. You typed {a!r}"
    glob_run(5, "challenge/words", [w for w in WORDS if "p" in w], rule)

@task("6 mixing globs")
def _():
    def rule(a):
        assert len(a) <= 6 and "[" in a, f"use a glob with [] of 6 characters or fewer. You typed {a!r}"
    glob_run(6, "challenge/words", ["challenging", "educational", "pwning"], rule)

@task("7 exclusionary globbing")
def _():
    def rule(a):
        assert "[!" in a or "[^" in a, f"use an exclusion glob like [!...]. You typed {a!r}"
    glob_run(7, "challenge/words", [w for w in WORDS if w[0] not in "pwn"], rule)

@task("8 tab completion")
def _():
    name = "pwncollege_" + word()
    root = dojo({"challenge/" + name: "x\n"})
    (root / "challenge/pwncollege").unlink()
    r, _ = go(8, root)
    assert lines(r) == [f"{root}/challenge/{name}"], f"print the completions of $DOJO/challenge/pwnc (the check renames the file) {show(r)}"

@task("9 multiple options for tab completion")
def _():
    extra = "pwncollege-f" + word(5)
    root = dojo({"challenge/tabfiles/" + extra: ""})
    want = sorted(f"{root}/challenge/tabfiles/{t}" for t in TABFILES + [extra] if t.startswith("pwncollege-f"))
    r, _ = go(9, root)
    assert sorted(lines(r)) == want, f"expected the {len(want)} completions of $DOJO/challenge/tabfiles/pwncollege-f {show(r)}"

@task("10 tab completion on commands")
def _():
    name = "pwncollege-" + word()
    root = dojo()
    (root / "bin/pwncollege-practice").rename(root / "bin" / name)
    r, _ = go(10, root)
    assert set(lines(r)) == {name}, f"print the command names that start with pwncollege (the check renames it to {name}) {show(r)}"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
