#!/bin/bash
find bin -type f -perm -4000 -printf '%f\n' | sort
