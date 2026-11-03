# Write a Local TCP Client: lesson

## Lesson

**Client and server.** A *server* waits for connections. A *client*
connects to the server. It sends a request and reads the answer. Here
`./run` starts a tiny test server on this computer. Then it runs your
`client.py` and tells it which port to use.

**Address and port.** `127.0.0.1` (*localhost*) is the address that
means "this same computer". So nothing leaves your machine. The *port* is
a number that picks one program on that computer. For example, a server
that listens on port 5000 only gets connections sent to port 5000. The
test server picks a free port at random each time. It passes the port to
your script.

**TCP and sockets.** TCP is a reliable two-way stream of bytes between
two programs. What one side sends arrives at the other side complete and
in order. A *socket* is the program's end of that connection. Inside the
system, a socket is a file descriptor (a number that names an open file or
connection), like in the earlier challenges. `send` and `recv` work in a
similar way to `write` and `read`.

**This challenge is in Python.** The course teaches Python in full later.
Here you only need a few lines. Python runs a `.py` file from top to
bottom (`python3 client.py 5000`). There is no compile step. The starter
already does this:

```python
import socket, sys          # load the socket and sys libraries
port = int(sys.argv[1])     # first command-line word, turned into a number
```

The Python you need:

- Indentation (spaces at the start of a line) groups lines into a block.
  It does the same job as `{ }` in C++. Lines inside a `with` block are
  indented 4 spaces.
- `b"hello\n"` is a *bytes* value. It is raw bytes. Sockets send bytes.
  `"hello"` without the `b` is text.
- `data.decode()` turns received bytes into text. `print(x)` prints it.
- `#` starts a comment.

Here are the socket calls. The example uses a different server and
message:

```python
with socket.create_connection(("127.0.0.1", 6000), timeout=3) as conn:
    conn.sendall(b"HELLO\n")    # send every byte
    reply = conn.recv(100)      # wait for up to 100 bytes back
    print(reply.decode())
```

- `create_connection` connects to an `(address, port)` pair. It gives
  back a connected socket.
- The `with` block closes the connection automatically at the end.
- `sendall` keeps sending until every byte is sent.
- `recv` returns the bytes that arrived. It returns an empty `b""` if the
  server closed the connection.

If no program listens on that port, you get `ConnectionRefusedError`.
Always connect to `127.0.0.1` only. The check expects a connection that
stays on this computer. When you run `./run`, it prints what your client
printed.

### New words

- **client / server**: the client is the side that connects. The server is the side that waits for connections.
- **IP address**: a computer's number on a network. `127.0.0.1` is this computer.
- **port**: a number that picks one program on a computer.
- **TCP**: a reliable two-way byte stream between two programs. Bytes arrive in order.
- **socket**: a program's end of a network connection.
- **bytes (`b"..."`)**: raw byte data in Python.
- **indentation**: leading spaces that group Python lines into a block.
- **decode**: turn bytes into text.
- **file descriptor**: a number that names an open file or connection.

## Offline help

- `man 7 tcp` (offline)
