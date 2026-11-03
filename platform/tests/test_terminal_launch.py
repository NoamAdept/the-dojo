"""Opening the learner's terminal on Windows (WSL): a Windows Terminal tab running bash in the distro."""

from __future__ import annotations

import os
import time
from pathlib import Path


def test_wsl_opens_windows_terminal_through_a_script(tmp_path, monkeypatch):
    from academy import terminal_launch as tl

    log = tmp_path / "argv.txt"
    fake = tmp_path / "bin"
    fake.mkdir()
    # A stand-in wt.exe: records its arguments, then runs the command after the tab options, like wt does.
    (fake / "wt.exe").write_text(
        '#!/bin/sh\nprintf "%s\\n" "$@" > "' + str(log) + '"\n'
        'shift 5\n[ "$1" = wsl.exe ] && shift 3\n[ "$1" = -e ] && shift\nexec "$@"\n'
    )
    (fake / "wt.exe").chmod(0o755)
    monkeypatch.setenv("PATH", f"{fake}:{os.environ['PATH']}")
    monkeypatch.setenv("WSL_DISTRO_NAME", "Ubuntu-24.04")
    monkeypatch.delenv("ACADEMY_OPEN_TERMINAL", raising=False)
    monkeypatch.setenv("SHELL", "/bin/true")
    ws = tmp_path / "my challenge; folder"
    ws.mkdir()

    res = tl.open_workspace_terminal(ws, challenge_id="lls-hello")
    assert res == {"ok": True, "via": "windows-terminal", "error": None}
    for _ in range(50):
        if log.exists() and log.read_text():
            break
        time.sleep(0.1)
    argv = log.read_text().splitlines()
    assert argv[:5] == ["-w", "0", "new-tab", "--title", "Signal Dojo"]
    assert argv[5:9] == ["wsl.exe", "-d", "Ubuntu-24.04", "-e"]
    # The folder (with its ; and space) only ever lives in the script, never on the Windows command line.
    assert argv[9] == "bash" and argv[10].endswith(".sh") and len(argv) == 11
    for _ in range(50):  # the script deletes itself once bash has read it
        if not Path(argv[10]).exists():
            break
        time.sleep(0.1)
    assert not Path(argv[10]).exists()


def test_is_wsl_reads_the_distro_variable(monkeypatch):
    from academy import terminal_launch as tl

    monkeypatch.setenv("WSL_DISTRO_NAME", "Ubuntu")
    assert tl.is_wsl()
