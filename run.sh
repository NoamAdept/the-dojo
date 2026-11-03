#!/bin/sh
# Closed-network launcher. Needs: python3 only. No pip. No internet.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname "$0")" && pwd)

# Windows laptops run Signal Dojo inside WSL (Ubuntu). See docs/WSL.md.
WSL=0
if [ -n "${WSL_DISTRO_NAME:-}" ] || grep -qi microsoft /proc/sys/kernel/osrelease 2>/dev/null; then
  WSL=1
fi
if [ "$WSL" = 1 ]; then
  case "$ROOT" in
    /mnt/[a-zA-Z]/*)
      if [ "${ACADEMY_ALLOW_WINDOWS_DRIVE:-0}" != 1 ]; then
        echo "Signal Dojo is in a Windows folder ($ROOT)." >&2
        echo "Windows folders lose Linux permissions, so many challenges break there." >&2
        echo "Unpack it in your Linux home folder instead, then run it from there:" >&2
        echo "  cd ~ && tar -xzf /mnt/c/Users/YOU/Downloads/pi-sdr-academy.tar.gz" >&2
        echo "  cd ~/pi-sdr-academy && ./run.sh" >&2
        echo "(ACADEMY_ALLOW_WINDOWS_DRIVE=1 ./run.sh starts it here anyway.)" >&2
        exit 1
      fi
      ;;
  esac
fi

# Prefer this folder's code — ignore user site-packages on the host.
export PYTHONNOUSERSITE=1
export PYTHONPATH="$ROOT/vendor:$ROOT/platform"

# Docker layout puts academy/ at ROOT
if [ ! -d "$ROOT/platform/academy" ] && [ -d "$ROOT/academy" ]; then
  export PYTHONPATH="$ROOT/vendor:$ROOT"
fi

export ACADEMY_CURRICULUM="${ACADEMY_CURRICULUM:-$ROOT/curriculum}"
export ACADEMY_DATA="${ACADEMY_DATA:-$ROOT/.academy-data}"
export ACADEMY_WORKSPACE="${ACADEMY_WORKSPACE:-$HOME/signal-dojo/challenge}"
export ACADEMY_FLAG_PATH="${ACADEMY_FLAG_PATH:-$ROOT/.academy-data/flag.txt}"

# The course teaches vim. Anything that opens an editor (git commit, crontab -e,
# sudoedit) gets vim, or vi where vim is missing; never the distro default.
_editor=vi
command -v vim >/dev/null 2>&1 && _editor=vim
export EDITOR="$_editor" VISUAL="$_editor" GIT_EDITOR="$_editor" SUDO_EDITOR="$_editor"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Signal Dojo needs python3 on PATH." >&2
  echo "No pip install required — only the python3 interpreter." >&2
  exit 1
fi

# Prove the pack is complete before opening the port.
if ! python3 -c "import yaml, academy"; then
  echo "Self-check failed: cannot import vendored yaml/academy." >&2
  echo "PYTHONPATH=$PYTHONPATH" >&2
  exit 1
fi

mkdir -p "$ACADEMY_DATA"
# Only the no-login console uses $ACADEMY_WORKSPACE. With logins every learner gets
# .academy-data/classroom/users/<name>/challenge (linked as ~/signal-dojo/<name>), and an
# empty ~/signal-dojo/challenge would only look like a challenge with its files missing.
case "${SINGLE_USER:-0}" in 1|true|yes) mkdir -p "$ACADEMY_WORKSPACE" ;; esac
chmod 700 "$ACADEMY_DATA" 2>/dev/null || true  # accounts and progress: this OS account only
# Everyone on the lab network can reach it by default; each learner logs in to their own account.
# HOST=127.0.0.1 ./run.sh keeps it to this machine. SINGLE_USER=1 ./run.sh is the old no-login console.
# On WSL the laptop is the learner's own: Windows reaches it as localhost, and WSL's own LAN
# address is not reachable from other computers anyway. HOST=0.0.0.0 ./run.sh still opens it up.
if [ "$WSL" = 1 ]; then
  HOST="${HOST:-127.0.0.1}"
else
  HOST="${HOST:-0.0.0.0}"
fi
PORT="${PORT:-8080}"

# Another Signal Dojo (often an older copy) already on this port: say so and stop, rather than
# opening the browser on that one and then failing with a traceback.
python3 -c 'import sys; from academy.api import check_port; check_port(sys.argv[1], int(sys.argv[2]))' "$HOST" "$PORT"

LAN_IP=""
if [ "$HOST" = "0.0.0.0" ]; then
  LAN_IP=$(hostname -I 2>/dev/null | awk '{print $1}') || LAN_IP=""
fi

echo ""
echo "  Signal Dojo  (offline / closed network)"
if [ -n "$LAN_IP" ]; then
  echo "  Open  http://$LAN_IP:$PORT/   (any computer on this network)"
  echo "        http://127.0.0.1:$PORT/   (this computer)"
elif [ "$WSL" = 1 ]; then
  echo "  Open  http://localhost:$PORT/   (in your Windows browser: Edge, Chrome, Firefox)"
else
  echo "  Open  http://$HOST:$PORT/"
fi
echo ""

# WSL: open the page in the Windows browser once the server is up (OPEN_BROWSER=0 ./run.sh skips it).
if [ "$WSL" = 1 ] && [ "${OPEN_BROWSER:-1}" = 1 ] && command -v cmd.exe >/dev/null 2>&1; then
  ( sleep 2; cd /mnt/c 2>/dev/null || true; cmd.exe /c start "http://localhost:$PORT/" >/dev/null 2>&1 || true ) &
fi

case "${ACADEMY_ADMIN:-0}" in
  1|true|yes)
    echo "  Admin http://127.0.0.1:$PORT/admin"
    exec python3 -m academy.cli admin --host "${ADMIN_HOST:-127.0.0.1}" --port "$PORT"
    ;;
esac
case "${SINGLE_USER:-0}" in
  1|true|yes)
    echo "  Then  Start (a terminal opens in $ACADEMY_WORKSPACE) → solve → Done"
    exec python3 -m academy.cli serve --local --host "$HOST" --port "$PORT"
    ;;
esac
echo "  Each learner: Create account (username + password) once, then Log in."
echo "  Progress saves by itself to that learner's own folder:"
echo "    $ACADEMY_DATA/classroom/users/<username>/"
echo "  The challenge files are in  ~/signal-dojo/<username>  (a link to that folder's challenge/)."
exec python3 -m academy.cli serve --host "$HOST" --port "$PORT"
