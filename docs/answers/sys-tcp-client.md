## Write a Local TCP Client

*sys-tcp-client · medium*

**Goal.** Finish `client.py` so it connects to the local test server on `127.0.0.1` at the port it is given, sends `PING`, and prints the `PONG` reply.

**You need to know.**

- Client, server, `127.0.0.1` and ports (README, "Client and server", "Address and port").
- `socket.create_connection((address, port), timeout=...)` inside a `with` block (README socket example).
- `b"..."` bytes, `sendall`, `recv` and `.decode()`.
- The starter already reads the port from `sys.argv[1]`.

**Walkthrough.**

1. Run the harness first to see how it works.

   ```bash
   ./run
   ```

   `./run` starts a tiny server on a random free port, then runs `python3 client.py <port>`. With the starter it just hangs, because the client exits without connecting and the server waits forever. Press Ctrl-C to stop it.

2. Open `client.py`. Keep the first three lines and replace the `# TODO` comment with:

   ```python
   with socket.create_connection(("127.0.0.1", port), timeout=3) as conn:
       conn.sendall(b"PING\n")
       reply = conn.recv(100)
       print(reply.decode().strip())
   ```

   - `create_connection` connects to the server on this computer only; `timeout=3` stops it hanging forever.
   - The server reads a line, so the request needs the `\n`, and it must be bytes (`b"..."`).
   - `recv(100)` waits for the reply; `decode()` turns it into text and `strip()` drops the newline before printing.
   - The `with` block closes the socket for us at the end.

3. Run it again.

   ```bash
   ./run
   ```

   It now prints `PONG`.

4. Run the check.

   ```bash
   ./check
   ```

   The check runs the same harness with a 5 second limit and looks for `PONG` in the output.

**Check.** `./check` prints `CHECK_OK`. Press Done in the dojo to get the flag.

**Common mistakes.**

- Sending `"PING\n"` (a str) instead of `b"PING\n"`: `sendall` raises `TypeError: a bytes-like object is required`.
- Forgetting to indent the lines under `with`, which gives `IndentationError`.
- `./run` hanging: the client never connected (crashed or still the stub). Ctrl-C, then run `python3 client.py 1` to see the Python error (it will say `ConnectionRefusedError` once the code is right, which is fine, since nothing listens on port 1).
