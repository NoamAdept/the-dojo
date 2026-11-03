#!/bin/bash
set -euo pipefail
directory=${1:?Usage: ./inventory.sh DIRECTORY}

shopt -s nullglob
{
  for path in "$directory"/*.iq; do
    name=$(basename "$path")
    size=$(stat -c %s "$path")
    hash=$(sha256sum "$path" | cut -d' ' -f1)
    printf '%s,%s,%s\n' "$name" "$size" "$hash"
  done
} | LC_ALL=C sort > manifest.txt
