#!/bin/sh
# Admin, once, on a Windows PC with internet: turn a fresh Ubuntu-24.04 WSL into The Dojo image.
# Inside that Ubuntu window:
#   tar -xzf /mnt/c/Users/YOU/Downloads/the-dojo.tar.gz -C ~
#   sh ~/the-dojo/wsl/build-image.sh
# Then in PowerShell:
#   wsl --shutdown
#   wsl --export Ubuntu-24.04 the-dojo-wsl.tar
# and copy the-dojo-wsl.tar + install-the-dojo.ps1 to each air-gapped laptop.
set -eu
HERE=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
# A git clone has the answers (solution/ folders). Every laptop gets this image, so stop here.
if [ -n "$(find "$HERE/../curriculum" -type d -name solution -print -quit 2>/dev/null)" ] \
   && [ "${DOJO_KEEP_ANSWERS:-0}" != 1 ]; then
  echo "This folder has the answers (it is a git clone). Learners could read them." >&2
  echo "Make the tarball and use that instead. See \"From GitHub\" in docs/WSL.md." >&2
  exit 1
fi
sh "$HERE/setup-ubuntu.sh"
# setup-ubuntu.sh already checked every tool; prove the academy itself starts.
"$HERE/../academy" --help >/dev/null
sudo apt-get clean   # smaller image: drop the downloaded .deb files
echo ""
echo "Image ready. In PowerShell:  wsl --shutdown ; wsl --export Ubuntu-24.04 the-dojo-wsl.tar"
