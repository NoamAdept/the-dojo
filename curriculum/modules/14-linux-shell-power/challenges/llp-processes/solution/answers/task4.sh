#!/bin/bash
p=$(cat pid.txt)
kill -STOP "$p"
sleep 0.2
ps -o stat= -p "$p" > state.txt
kill -CONT "$p"
