#!/bin/bash
find box -type f -perm -o=r -printf '%f\n' | sort
