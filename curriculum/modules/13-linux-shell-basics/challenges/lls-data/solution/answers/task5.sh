#!/bin/bash
"$DOJO/challenge/columns" | cut -d " " -f 2 | tr -d "\n"
