#!/usr/bin/env python3
import socket
import sys

def request_reading(host, port, channel):
    with socket.create_connection((host, port), timeout=3) as s:
        s.sendall(f"READ {channel}\n".encode())
        chunks = []
        while True:
            piece = s.recv(4096)
            if piece == b"":
                break
            chunks.append(piece)
    return b"".join(chunks).decode().strip()

if __name__ == "__main__":
    print(request_reading(sys.argv[1], int(sys.argv[2]), int(sys.argv[3])))
