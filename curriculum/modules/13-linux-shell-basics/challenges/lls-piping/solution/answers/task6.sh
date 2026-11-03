#!/bin/bash
"$DOJO/challenge/noisy" > "$DOJO/tmp/data.txt"
grep "academy{" "$DOJO/tmp/data.txt"
