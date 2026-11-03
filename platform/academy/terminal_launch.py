"""Open a local terminal focused on a challenge workspace."""

from __future__ import annotations

import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path


def open_workspace_terminal(workspace: str | Path, *, challenge_id: str = "") -> dict:
    """
    Launch a visible terminal with cwd=workspace.
    Returns {"ok": bool, "via": str|None, "error": str|None}.
    Set ACADEMY_OPEN_TERMINAL=0 to disable.
    """
    if os.environ.get("ACADEMY_OPEN_TERMINAL", "1").strip().lower() in {"0", "false", "no", "off"}:
        return {"ok": False, "via": None, "error": "disabled by ACADEMY_OPEN_TERMINAL"}

    dest = Path(workspace).expanduser().resolve()
    if not dest.is_dir():
        return {"ok": False, "via": None, "error": f"workspace missing: {dest}"}

    label = challenge_id or dest.name
    # The course teaches vim: git commit, crontab -e, sudoedit and friends must
    # open vim (or vi), never the distro default editor.
    editor = (
        "_e=vi; command -v vim >/dev/null 2>&1 && _e=vim; "
        'export EDITOR="$_e" VISUAL="$_e" GIT_EDITOR="$_e" SUDO_EDITOR="$_e"; unset _e; '
    )
    # Hard-clear scrollback + screen, then a tiny banner (no wall of text).
    clear = r"printf '\033c\033[3J'; clear 2>/dev/null; "
    banner = (
        clear
        + editor
        + f"printf '\\033[1;92m%s\\033[0m  \\033[1;96m%s\\033[0m\\n' '道場' {shlex.quote(label)}; "
        + "printf '\\033[2m%s\\033[0m\\n\\n' 'ls · cat README* · ./check'; "
        + 'exec "$SHELL" -l'
    )
    shell_cmd = f"cd {shlex.quote(str(dest))} && {banner}"

    try:
        if sys.platform == "darwin":
            via = _open_macos(shell_cmd)
        elif is_wsl():
            # WSL (Windows laptops): a Windows Terminal tab in this distro. Ubuntu on WSL has no Linux
            # terminal app, so fall back to one only if the Windows side cannot open a window.
            via = _open_wsl(shell_cmd) or _open_linux(shell_cmd, dest)
        else:
            via = _open_linux(shell_cmd, dest)
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "via": None, "error": str(exc)}

    if via:
        return {"ok": True, "via": via, "error": None}
    return {"ok": False, "via": None, "error": "no terminal app found"}


def is_wsl() -> bool:
    """True inside Windows Subsystem for Linux (WSL 1 or 2)."""
    if os.environ.get("WSL_DISTRO_NAME"):
        return True
    try:
        return "microsoft" in Path("/proc/sys/kernel/osrelease").read_text(encoding="utf-8").lower()
    except OSError:
        return False


def _windows_exe(name: str, fallback: str) -> str | None:
    found = shutil.which(name)
    if found:
        return found
    return fallback if fallback and Path(fallback).exists() else None


def _open_wsl(shell_cmd: str) -> str | None:
    """Open a Windows Terminal tab (or a console window) running bash in this WSL distro.

    The command goes through a small script file, never on the Windows command line: wt.exe treats
    `;` as its own separator and cmd.exe re-parses quotes, so passing shell text through either breaks.
    """
    import tempfile

    fd, script = tempfile.mkstemp(prefix="the-dojo-term-", suffix=".sh")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write('rm -f "$0"\n' + shell_cmd + "\n")
    os.chmod(script, 0o700)
    distro = os.environ.get("WSL_DISTRO_NAME", "")
    inner = ["wsl.exe"] + (["-d", distro] if distro else []) + ["-e", "bash", script]
    # Windows programs complain when started from a Linux folder; start them from C:\ instead.
    cwd = "/mnt/c" if Path("/mnt/c").is_dir() else None
    attempts = []
    wt = _windows_exe("wt.exe", "")
    if wt:
        attempts.append(("windows-terminal", [wt, "-w", "0", "new-tab", "--title", "The Dojo", *inner]))
    cmd = _windows_exe("cmd.exe", "/mnt/c/Windows/System32/cmd.exe")
    if cmd:
        attempts.append(("wsl-console", [cmd, "/c", "start", "The Dojo", *inner]))
    for via, argv in attempts:
        try:
            subprocess.Popen(  # noqa: S603
                argv,
                cwd=cwd,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
            return via
        except OSError:
            continue
    try:
        os.unlink(script)
    except OSError:
        pass
    return None


def _as_quote(s: str) -> str:
    """AppleScript double-quoted string literal."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _open_macos(shell_cmd: str) -> str | None:
    if shutil.which("osascript") is None:
        return None

    q = _as_quote(shell_cmd)

    iterm = Path("/Applications/iTerm.app")
    if iterm.exists() or _app_running("iTerm2") or _app_running("iTerm"):
        script = f"""
tell application "iTerm"
  activate
  if (count of windows) = 0 then
    create window with default profile
  else
    tell current window
      create tab with default profile
    end tell
  end if
  tell current session of current window
    write text {q}
  end tell
end tell
"""
        if _run_osascript(script):
            return "iterm"

    script = f"""
tell application "Terminal"
  activate
  do script {q}
end tell
"""
    if _run_osascript(script):
        return "terminal.app"
    return None


def _app_running(name: str) -> bool:
    try:
        r = subprocess.run(
            ["pgrep", "-x", name],
            capture_output=True,
            check=False,
        )
        return r.returncode == 0
    except OSError:
        return False


def _run_osascript(script: str) -> bool:
    r = subprocess.run(
        ["osascript"],
        input=script,
        text=True,
        capture_output=True,
        check=False,
    )
    return r.returncode == 0


def _open_linux(shell_cmd: str, dest: Path) -> str | None:
    if not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")):
        return None  # headless (SSH, Docker): no window can open; the page shows the folder instead
    candidates = [
        ("lxterminal", ["lxterminal", f"--working-directory={dest}", "-e", f"bash -lc {shlex.quote(shell_cmd)}"]),
        ("xfce4-terminal", ["xfce4-terminal", f"--working-directory={dest}", "-e", f"bash -lc {shlex.quote(shell_cmd)}"]),
        ("gnome-terminal", ["gnome-terminal", f"--working-directory={dest}", "--", "bash", "-lc", shell_cmd]),
        ("konsole", ["konsole", "--workdir", str(dest), "-e", "bash", "-lc", shell_cmd]),
        ("x-terminal-emulator", ["x-terminal-emulator", "-e", f"bash -lc {shlex.quote(shell_cmd)}"]),
        ("xterm", ["xterm", "-e", f"bash -lc {shlex.quote(shell_cmd)}"]),
    ]
    for name, argv in candidates:
        if not shutil.which(argv[0]):
            continue
        try:
            subprocess.Popen(  # noqa: S603
                argv,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
            return name
        except OSError:
            continue
    return None
