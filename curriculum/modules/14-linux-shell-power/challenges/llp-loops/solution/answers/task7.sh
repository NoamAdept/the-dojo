#!/bin/bash
shopt -s nullglob
for f in "$1"/*.txt; do
    echo "$(stat -c %s "$f") $(basename "$f")"
done | sort -n
