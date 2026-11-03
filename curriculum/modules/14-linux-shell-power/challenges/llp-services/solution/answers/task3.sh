#!/bin/bash
for p in $(cat ports.txt); do
    if curl -s -o /dev/null "http://127.0.0.1:$p/"; then
        echo "$p"
    fi
done
