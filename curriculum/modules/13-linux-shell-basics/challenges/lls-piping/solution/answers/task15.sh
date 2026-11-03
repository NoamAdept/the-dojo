#!/bin/bash
mkfifo "$DOJO/tmp/flag_fifo"
"$DOJO/challenge/fifo" > "$DOJO/tmp/flag_fifo" &
cat "$DOJO/tmp/flag_fifo"
wait
