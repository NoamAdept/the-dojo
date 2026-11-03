#!/bin/bash
shopt -s nullglob
count=0
for f in "$1"/*.log; do
    count=$((count + 1))
done
echo "$count"
