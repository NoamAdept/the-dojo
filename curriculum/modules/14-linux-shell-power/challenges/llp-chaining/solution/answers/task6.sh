#!/bin/bash
if [ "$1" -lt 0 ]; then
    echo negative
elif [ "$1" -eq 0 ]; then
    echo zero
elif [ "$1" -lt 10 ]; then
    echo small
else
    echo large
fi
