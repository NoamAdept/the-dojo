#!/bin/bash
"$DOJO/challenge/pwn" --secret pipeline7 | tee ~/pwn.log | "$DOJO/challenge/college"
