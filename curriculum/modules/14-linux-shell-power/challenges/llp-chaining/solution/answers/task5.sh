#!/bin/bash
if [ -f "$1" ]; then
    echo "found $1"
else
    echo "missing $1"
    exit 1
fi
