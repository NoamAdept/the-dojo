#!/bin/bash
shopt -s nullglob
total=0
for f in "$1"/*.dat; do
    total=$((total + $(stat -c %s "$f")))
done
echo "$total"
