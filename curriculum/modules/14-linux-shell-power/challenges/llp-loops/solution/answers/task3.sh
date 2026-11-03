#!/bin/bash
shopt -s nullglob
for f in "$1"/*.txt; do
    cp "$f" "$2/$(basename "$f").bak"
done
