## Talk to a Local Signal Server

*py-socket-client · medium*

**Goal.** Complete `request_reading(host, port, channel)` in `client.py` so it connects, sends `READ <channel>\n`, keeps reading until the server closes, and returns the whole reply as stripped text.

**You need to know.**

- Host, port and `socket.create_connection((host, port), timeout=3)` (README lessons 2 and 3, and sys-tcp-client).
- `.encode()` before sending and `.decode()` after receiving (README lesson 4).
- One `recv` may return only part of the reply; loop until it returns `b""` (README lesson 5).
- The exact request format `READ 7\n` (README lesson 6).

**Walkthrough.**

1. Try the starter.

   ```bash
   ./run
   ```

   It prints an empty line and then `The client did not connect to the local practice server.`, because the stub returns `""` without connecting.

2. Replace the `# TODO` and `return ""` in `request_reading` with:

   ```python
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
   ```

   - Use the `host` and `port` arguments, never a typed port number, because the harness picks a free port each time.
   - The f-string builds exactly `READ 7\n`, and `.encode()` turns it into bytes for `sendall`.
   - The server sends its answer in two pieces, so we keep calling `recv` and collect every piece; `b""` means the server closed, so we stop.
   - `b"".join` glues the pieces, `decode` makes text, and `strip` removes the final newline.

3. Leave the main block as it is and run the harness.

   ```bash
   ./run
   ```

   It prints `channel=7 power=-38`.

4. Run the check.

   ```bash
   ./check
   ```

   The check starts its own server, asks for channel 12, and verifies both the exact request bytes and the full reply.

**Check.** `./check` prints `CHECK_OK`. Press Done in the dojo to get the flag.

**Common mistakes.**

- A single `recv` with no loop: the function returns only `channel=7` (the first piece), and the check says "receive and return the complete stripped reply".
- Wrong request text, like `READ7\n`, `read 7\n`, or no newline (the server then waits forever and the client times out).
- Returning without `.strip()`, so the reply ends in `\n` and does not match.
