#!/usr/bin/env python3
import socket, sys
port=int(sys.argv[1])
with socket.create_connection(("127.0.0.1", port), timeout=3) as conn:
    conn.sendall(b"PING\n")
    reply = conn.recv(100)
    print(reply.decode().strip())
