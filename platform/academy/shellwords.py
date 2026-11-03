"""Split a bash script into the simple commands bash would run, for ./check scripts.

A few shell checks must look at *how* a learner called a program (which glob they typed,
which path form they used), not only at what it printed. They read the answer script with
`invocations()` instead of comparing strings, so quoting, extra spaces, `&&`, `;`, pipes,
redirections, comments and `VAR=value` prefixes do not matter.

Each challenge folder must work on its own (learners run `./check` with plain python3),
so the check.py files that need this carry a copy of the block between the markers below.
platform/tests/test_shellwords.py fails if a copy drifts from this file.
"""

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
