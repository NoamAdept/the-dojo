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
sh "$HERE/setup-ubuntu.sh"
# setup-ubuntu.sh already checked every tool; prove the academy itself starts.
"$HERE/../academy" --help >/dev/null
sudo apt-get clean   # smaller image: drop the downloaded .deb files
echo ""
echo "Image ready. In PowerShell:  wsl --shutdown ; wsl --export Ubuntu-24.04 the-dojo-wsl.tar"
