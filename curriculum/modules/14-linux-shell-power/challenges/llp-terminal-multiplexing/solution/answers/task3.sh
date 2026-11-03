#!/bin/bash
tmux send-keys -t "$(cat name.txt)" "echo $(cat token.txt) > out.txt" Enter
