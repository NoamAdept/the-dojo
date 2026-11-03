"""The shell-script reader that the path and glob checks use instead of string matching."""

from __future__ import annotations

import time
from pathlib import Path

import pytest

from academy import shellwords
from academy.shellwords import invocations, shell_commands

ROOT = Path(__file__).resolve().parents[2]
BEGIN, END = "# --- shellwords: begin", "# --- shellwords: end ---"


def block(text: str) -> str:
    return text[text.index(BEGIN):text.index(END) + len(END)]


def test_every_check_carries_the_same_copy():
    """Checks are standalone files, so they hold a copy; it must match the tested original."""
    want = block(Path(shellwords.__file__).read_text())
    copies = [p for p in ROOT.glob("curriculum/modules/*/challenges/*/files/check.py") if BEGIN in p.read_text()]
    assert copies, "no check uses shellwords"
    for p in copies:
        assert block(p.read_text()) == want, f"{p.relative_to(ROOT)} has an old copy of shellwords: run scripts/sync_shellwords.py"


@pytest.mark.parametrize("script, want", [
    ("", []),
    ("   \n\n\t\n", []),
    ("# only a comment", []),
    ("ls", [["ls"]]),
    ("ls -la", [["ls", "-la"]]),
    ("ls   -l    -a   /tmp/  ", [["ls", "-l", "-a", "/tmp/"]]),
    ("ls --all ~", [["ls", "--all", "~"]]),
    ("ls -la # list it", [["ls", "-la"]]),
    ("echo a#b", [["echo", "a#b"]]),
    ("cd /tmp; ls && pwd || whoami", [["cd", "/tmp"], ["ls"], ["pwd"], ["whoami"]]),
    ("cat f | grep x | sort -u", [["cat", "f"], ["grep", "x"], ["sort", "-u"]]),
    ("sleep 1 & wait", [["sleep", "1"], ["wait"]]),
    ("echo 'a b' \"c d\" e\\ f", [["echo", "a b", "c d", "e f"]]),
    ('cd "$DOJO"/ch*', [["cd", "$DOJO/ch*"]]),
    ("cd \"${DOJO}/\"'ch'*", [["cd", "${DOJO}/ch*"]]),
    ("echo hi > out.txt 2>&1", [["echo", "hi"]]),
    ("run file_[ab] 2>/dev/null", [["run", "file_[ab]"]]),
    ("echo 2 > f", [["echo", "2"]]),
    ("sort < in > out", [["sort"]]),
    ("cmd &> log; other >> log", [["cmd"], ["other"]]),
    ("PWN=COLLEGE", []),
    ("PWN=COLLEGE run", [["run"]]),
    ("export PWN=COLLEGE", [["export", "PWN=COLLEGE"]]),
    ("env A=1 B=2 prog x", [["prog", "x"]]),
    ("command -v ls", [["-v", "ls"]]),
    ("if [ -f x ]; then echo yes; else echo no; fi", [["[", "-f", "x", "]"], ["echo", "yes"], ["echo", "no"]]),
    ("for f in *.txt; do wc -l \"$f\"; done", [["wc", "-l", "$f"]]),
    ("while read l; do echo $l; done < file", [["read", "l"], ["echo", "$l"]]),
    ("[[ -f $1 ]] && echo found", [["echo", "found"]]),
    ("x=$(whoami)", [["whoami"]]),
    ('echo "me: $(id -un)"', [["id", "-un"], ["echo", "me: $(id -un)"]]),
    ("echo `date`", [["date"], ["echo", "`date`"]]),
    ("diff <(a 1) <(b 2)", [["a", "1"], ["b", "2"], ["diff", "<(a 1)", "<(b 2)"]]),
    ("tee >(the) | planet", [["the"], ["tee", ">(the)"], ["planet"]]),
    ("echo $((1 + 2))", [["echo", "$((1 + 2))"]]),
    ("(cd /tmp && ls)", [["cd", "/tmp"], ["ls"]]),
    ("ls \\\n  -la", [["ls", "-la"]]),
    ("cat > f <<'EOF'\nrm -rf /\nEOF\nls", [["cat"], ["ls"]]),
    ("cat <<-END\n\tnot a command\n\tEND\nls", [["cat"], ["ls"]]),
    ('echo "a << b"; ls', [["echo", "a << b"], ["ls"]]),
    ("tr a b <<< 'x'; ls", [["tr", "a", "b"], ["ls"]]),
])
def test_shell_commands(script, want):
    assert shell_commands(script) == want


def test_unfinished_quotes_do_not_crash():
    assert shell_commands("echo 'not closed") == [["echo", "not closed"]]
    assert shell_commands('echo "not closed') == [["echo", "not closed"]]
    assert shell_commands("echo $(not closed") == [["not", "closed"], ["echo", "$(not closed"]]


def test_unknown_commands_are_just_words():
    assert shell_commands("frobnicate --wibble=3 x") == [["frobnicate", "--wibble=3", "x"]]


def test_very_long_input_is_fast():
    script = "\n".join(f'cd "$DOJO/d{i}" && ls -la "file {i}" | grep -v x > out{i} 2>&1' for i in range(5000))
    start = time.time()
    cmds = shell_commands(script)
    assert len(cmds) == 15000
    assert time.time() - start < 5


@pytest.mark.parametrize("script, prog, want", [
    ('"$DOJO/challenge/run" a', "run", [["a"]]),
    ("./run a; ../run b; run c; /x/y/run d", "run", [["a"], ["b"], ["c"], ["d"]]),
    ("rerun x; runner y", "run", []),
    ("cd $DOJO/challenge/ && ./copyflag ~/f", "copyflag", [["~/f"]]),
    ("cd a; cd; cd b/", "cd", [["a"], [], ["b/"]]),
])
def test_invocations(script, prog, want):
    assert invocations(script, prog) == want
