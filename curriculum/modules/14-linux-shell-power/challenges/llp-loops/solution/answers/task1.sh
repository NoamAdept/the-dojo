#!/bin/bash
shopt -s nullglob
for f in "$1"/*.txt; do
    basename "$f"
done
