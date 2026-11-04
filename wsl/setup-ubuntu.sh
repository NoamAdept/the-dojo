#!/bin/sh
# Prepare Ubuntu on WSL for The Dojo. Run it inside the Ubuntu window, as your normal user,
# on a machine with internet (once, when you build the image you hand out; see docs/WSL.md):
#
#   tar -xzf /mnt/c/Users/YOU/Downloads/the-dojo.tar.gz -C ~
#   sh ~/the-dojo/wsl/setup-ubuntu.sh
#
# It installs the lab packages, makes vim the editor, turns on systemd (Yellow belt services),
# makes you the default user (so an exported/imported copy does not log in as root), and adds
# a `dojo` command that starts the academy. Safe to run again.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)

case "$ROOT" in
  /mnt/[a-zA-Z]/*)
    echo "Put The Dojo in your Linux home first (cd ~ && tar -xzf .../the-dojo.tar.gz). See docs/WSL.md." >&2
    exit 1 ;;
esac
if [ "$(id -u)" = 0 ]; then
  echo "Run this as your normal Ubuntu user (it uses sudo where it must), not as root." >&2
  exit 1
fi

# The terminal, C++, gdb and Python: every challenge's expected tools are here.
PACKAGES="vim tmux curl less man-db manpages manpages-dev build-essential gdb cmake pkg-config git \
python3 tree net-tools netcat-openbsd iproute2 lsof procps psmisc"

if [ "${SKIP_APT:-0}" != 1 ]; then
  sudo apt-get update
  # shellcheck disable=SC2086
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y $PACKAGES
fi
sudo update-alternatives --set editor /usr/bin/vim.basic 2>/dev/null || true

# /etc/wsl.conf: systemd on, this user by default. Other settings in the file are kept.
sudo python3 - "$(id -un)" <<'PY'
import configparser, sys
from pathlib import Path
path = Path("/etc/wsl.conf")
cfg = configparser.ConfigParser()
cfg.optionxform = str
if path.exists():
    cfg.read(path)
for section, key, value in (("boot", "systemd", "true"), ("user", "default", sys.argv[1])):
    if not cfg.has_section(section):
        cfg.add_section(section)
    cfg[section][key] = value
with path.open("w") as fh:
    cfg.write(fh)
print("wrote /etc/wsl.conf:", dict(cfg["boot"]), dict(cfg["user"]))
PY

# `dojo` starts the academy from anywhere.
mkdir -p "$HOME/.local/bin"
cat > "$HOME/.local/bin/dojo" <<SH
#!/bin/sh
exec "$ROOT/run.sh" "\$@"
SH
chmod 755 "$HOME/.local/bin/dojo"

missing=""
for tool in python3 g++ gdb cmake tmux vim man tree netstat nc ss; do
  command -v "$tool" >/dev/null 2>&1 || missing="$missing $tool"
done
if [ -n "$missing" ]; then
  echo "Still missing:$missing" >&2
  exit 1
fi
echo ""
echo "Ready. Close this window, run  wsl --shutdown  in PowerShell (so systemd starts),"
echo "open Ubuntu again and type:  dojo"
