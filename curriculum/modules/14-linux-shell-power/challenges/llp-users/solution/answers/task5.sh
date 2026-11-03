#!/bin/bash
awk -F: '$3 >= 1000 && $3 != 65534 {print $1, $3}' passwd.txt | sort -k2,2n
