# Local Wire Tap

`sys-tcp-client` · Blue Belt

**Goal:** Finish `client.py` so it connects to the local test server on `127.0.0.1` at the port it is given, sends `PING`, and prints the `PONG` reply.

**File `client.py`**

```python
import socket, sys
port=int(sys.argv[1])
with socket.create_connection(("127.0.0.1", port), timeout=3) as conn:
    conn.sendall(b"PING\n")
    reply = conn.recv(100)
    print(reply.decode().strip())
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
