#!/bin/bash
python3 -m http.server "$(cat port.txt)" --bind 127.0.0.1 > server.log 2>&1 &
echo $! > server.pid
