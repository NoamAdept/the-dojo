#!/usr/bin/env python3
"""Run with ./check. Tests each task in answers/task1.sh to answers/task15.sh and lists what still fails."""
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
RNG = random.Random(106)


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

TREE = {}
PROGS = {'challenge/run': '#!/bin/bash\necho "instructions: I print the secret on stdout and these words on stderr" >&2\necho "@SECRET@"\n', 'challenge/append': '#!/bin/bash\nprintf "%s" "@A@" > "$HOME/the-flag"\nprintf "%s\\n" "@B@"\n', 'challenge/needinput': '#!/bin/bash\n[ -f /dev/stdin ] || { echo "needinput: redirect a FILE into my stdin with <" >&2; exit 1; }\nread -r line\n[ "$line" = COLLEGE ] || { echo "needinput: the file should contain COLLEGE, I read \'$line\'" >&2; exit 1; }\necho "needinput OK ${TOKEN:-practice}"\n', 'challenge/noisy': '#!/bin/bash\nnoise() { seq "$1" "$2" | sed \'s/^/just some noise, line /\'; }\n{ noise 1 @POS@; echo "@SECRET@"; noise $((@POS@ + 1)) 20000; } \n', 'challenge/noisyerr': '#!/bin/bash\nnoise() { seq "$1" "$2" | sed \'s/^/just some noise, line /\'; }\n{ noise 1 @POS@; echo "@SECRET@"; noise $((@POS@ + 1)) 20000; } >&2\n', 'challenge/decoys': '#!/bin/bash\nfake() { seq "$1" "$2" | sed -e \'s/^\\(.*[02468]\\)$/academy{DECOY_\\1}/\' -e \'s/^\\([0-9]*[13579]\\)$/academy{\\1_DECOY}/\'; }\n{ fake 1 @POS@; echo "@SECRET@"; fake $((@POS@ + 1)) 1000; }\n', 'challenge/fakeflag': '#!/bin/bash\necho "@FAKE@"\n', 'challenge/pwn': '#!/bin/bash\nif [ "$1" != --secret ] || [ "$2" != pipeline7 ]; then\n    echo "Usage: pwn --secret SECRET_ARG"\n    echo "SECRET_ARG should be pipeline7"\n    exit 2\nfi\necho "SUPERSECRET:@CODE@"\n', 'challenge/college': '#!/bin/bash\ndata=$(cat)\ncase "$data" in\n    *"SUPERSECRET:@CODE@"*) echo "college OK ${TOKEN:-practice}";;\n    *) echo "college: my input did not contain the right SUPERSECRET code. Use tee to see what pwn printed." >&2; exit 2;;\nesac\n', 'challenge/print_decoys': '#!/bin/bash\nfake() { seq "$1" "$2" | sed -e \'s/^\\(.*[02468]\\)$/academy{DECOY_\\1}/\' -e \'s/^\\([0-9]*[13579]\\)$/academy{\\1_DECOY}/\'; }\n{ fake 1 @POS@;  fake $((@POS@ + 1)) 1000; }\n', 'challenge/print_decoys_and_flag': '#!/bin/bash\nfake() { seq "$1" "$2" | sed -e \'s/^\\(.*[02468]\\)$/academy{DECOY_\\1}/\' -e \'s/^\\([0-9]*[13579]\\)$/academy{\\1_DECOY}/\'; }\n{ fake 1 @POS@; echo "@SECRET@"; fake $((@POS@ + 1)) 1000; }\n', 'challenge/hack': '#!/bin/bash\necho "@OUT@"\necho "@ERR@" >&2\n', 'challenge/the': '#!/bin/bash\nprintf "the got %s\\n" "$(cat)"\n', 'challenge/planet': '#!/bin/bash\nprintf "planet got %s\\n" "$(cat)"\n', 'challenge/fifo': '#!/bin/bash\n[ /dev/stdout -ef "$DOJO/tmp/flag_fifo" ] && [ -p "$DOJO/tmp/flag_fifo" ] || {\n    echo "fifo: my stdout must be redirected into the named pipe $DOJO/tmp/flag_fifo" >&2; exit 1; }\necho "@SECRET@"\n'}
PRACTICE = {'@SECRET@': 'academy{practice_pipe}', '@A@': 'academy{practice_', '@B@': 'append_ok}xxxxxxx', '@FAKE@': 'aFAKEFLAGcFAKEFLAGaFAKEFLAGdFAKEFLAGeFAKEFLAGmFAKEFLAGyFAKEFLAG{FAKEFLAGpFAKEFLAGrFAKEFLAGaFAKEFLAGcFAKEFLAGtFAKEFLAGiFAKEFLAGcFAKEFLAGeFAKEFLAG_FAKEFLAGsFAKEFLAGeFAKEFLAGdFAKEFLAG}', '@CODE@': 'practice', '@OUT@': 'out-practice', '@ERR@': 'err-practice', '@POS@': '400'}


def subs(**kw):
    s = {"@SECRET@": secret("pipe"), "@POS@": str(RNG.randint(100, 900))}
    s.update(kw)
    return s

def home(root):
    return root / "home/hacker"

@task("1 redirecting output")
def _():
    root = dojo()
    r, _ = go(1, root)
    f = home(root) / "COLLEGE"
    assert f.is_file(), f"no file named COLLEGE in your home directory {show(r)}"
    assert f.read_text().strip() == "PWN", f"COLLEGE should contain PWN. It contains {f.read_text()!r}"

@task("2 redirecting more output")
def _():
    s = subs()
    root = dojo(subs=s)
    r, _ = go(2, root)
    f = home(root) / "myflag"
    assert f.is_file() and f.read_text().strip() == s["@SECRET@"], f"~/myflag should hold run's stdout {show(r)}"

@task("3 appending output")
def _():
    a, b = "academy{" + word(9), word(9) + "}"
    root = dojo(subs={"@A@": a, "@B@": b})
    r, _ = go(3, root)
    f = home(root) / "the-flag"
    assert f.is_file(), f"~/the-flag does not exist {show(r)}"
    assert f.read_text() == a + b + "\n", f"~/the-flag holds {f.read_text()!r}. Use >> to append to the file"

@task("4 redirecting errors")
def _():
    s = subs()
    root = dojo(subs=s)
    r, _ = go(4, root)
    out, err = home(root) / "myflag", home(root) / "instructions"
    assert out.is_file() and out.read_text().strip() == s["@SECRET@"], f"~/myflag should hold stdout {show(r)}"
    assert err.is_file() and "instructions" in err.read_text(), "~/instructions should hold stderr"

@task("5 redirecting input")
def _():
    root = dojo()
    r, tok = go(5, root)
    f = home(root) / "PWN"
    assert f.is_file() and f.read_text().strip() == "COLLEGE", f"~/PWN should contain COLLEGE {show(r)}"
    assert f"needinput OK {tok}" in r.stdout, f"redirect ~/PWN into needinput with < {show(r)}"

@task("6 grepping stored results")
def _():
    s = subs()
    root = dojo(subs=s)
    r, _ = go(6, root)
    f = root / "tmp/data.txt"
    assert f.is_file() and len(f.read_text().splitlines()) == 20001, f"$DOJO/tmp/data.txt should hold all of noisy's output {show(r)}"
    assert r.stdout.strip() == s["@SECRET@"], f"then print only the academy{{ line {show(r)}"

@task("7 grepping live output")
def _():
    s = subs()
    r, _ = go(7, dojo(subs=s))
    assert r.stdout.strip() == s["@SECRET@"], f"pipe noisy into grep and print only the academy{{ line {show(r)}"

@task("8 grepping errors")
def _():
    s = subs()
    r, _ = go(8, dojo(subs=s))
    assert r.stdout.strip() == s["@SECRET@"], f"noisyerr writes to stderr. Send stderr into the pipe with 2>&1 {show(r)}"

@task("9 filtering with grep -v")
def _():
    s = subs()
    r, _ = go(9, dojo(subs=s))
    assert r.stdout.strip() == s["@SECRET@"], f"remove every line containing DECOY {show(r)}"

@task("10 filtering with sed")
def _():
    s = secret("sed")
    r, _ = go(10, dojo(subs={"@FAKE@": "FAKEFLAG".join(s)}))
    assert r.stdout.strip() == s, f"delete every FAKEFLAG with sed {show(r)}"

@task("11 duplicating piped data with tee")
def _():
    code = word()
    root = dojo(subs={"@CODE@": code})
    r, tok = go(11, root)
    log = home(root) / "pwn.log"
    assert log.is_file(), f"save a copy of what flows through the pipe in ~/pwn.log with tee {show(r)}"
    assert f"SUPERSECRET:{code}" in log.read_text(), f"~/pwn.log holds {log.read_text()[:200]!r}. Did pwn get the arguments it asks for?"
    assert f"college OK {tok}" in r.stdout, f"pipe pwn's output (through tee) into college {show(r)}"

@task("12 process substitution for input")
def _():
    s = subs()
    r, _ = go(12, dojo(subs=s))
    assert s["@SECRET@"] in r.stdout, f"diff the outputs of the 2 programs {show(r)}"
    assert r.stdout.count("DECOY") == 0, "print only the difference, not the decoys"
    used = [w for args in invocations(script(12), "diff") for w in args]
    assert any(w.startswith("<(") for w in used), "use process substitution: diff <(command 1) <(command 2)"

def hack(n, want_the, want_planet):
    out, err = "out-" + word(), "err-" + word()
    r, _ = go(n, dojo(subs={"@OUT@": out, "@ERR@": err}))
    got = lines(r)
    exp_the = "the got " + (out if want_the == "out" else err)
    exp_planet = "planet got " + (out if want_planet == "out" else err)
    assert exp_the in got, f"the should receive hack's std{want_the} {show(r)}"
    assert exp_planet in got, f"planet should receive hack's std{want_planet} {show(r)}"

@task("13 writing to multiple programs")
def _():
    hack(13, "out", "out")

@task("14 split-piping stderr and stdout")
def _():
    hack(14, "err", "out")

@task("15 named pipes")
def _():
    s = subs()
    root = dojo(subs=s)
    r, _ = go(15, root, timeout=8)
    f = root / "tmp/flag_fifo"
    assert f.is_fifo(), f"$DOJO/tmp/flag_fifo should be a named pipe made with mkfifo {show(r)}"
    assert s["@SECRET@"] in r.stdout, f"read the secret out of the FIFO (for example with cat) {show(r)}"

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
