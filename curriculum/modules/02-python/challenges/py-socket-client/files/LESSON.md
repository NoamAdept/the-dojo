# Talk to a Local Socket: lesson

### 1. Client and server

A server is a program that waits for other programs to connect. A client
is a program that connects to the server and asks for something. Here the
`./run` and `./check` scripts start a tiny server on your own computer.
Your client.py talks to it. Nothing leaves your machine.

### 2. Host and port

To connect you need two things:

- **host**: which computer. "127.0.0.1" (also called localhost) means
  "this same computer".
- **port**: which program on that computer. It is a number like 50123.

`./run` and `./check` pick a free port. They pass the host, port and
channel to your function. So never type a port number into your code.

### 3. TCP sockets

A socket is the program's end of a network connection. Here you use a
TCP connection. TCP delivers bytes in order, and no bytes are lost.

```
import socket
with socket.create_connection((host, port), timeout=3) as s:
    ...                      # talk here; closed automatically after
```

Note the double brackets. (host, port) is one tuple argument. (A tuple
is a fixed list in round brackets.)
`timeout=3` means "stop waiting after 3 seconds". Without it, the program
could wait forever.

### 4. Sockets send bytes, not strings

Turn text into bytes with .encode(). Turn bytes back into text with
.decode():

```
"hi\n".encode()      # b'hi\n'
b"ok".decode()       # 'ok'
```

Send everything with s.sendall(some_bytes). The server reads until it
sees a newline "\n". So your request must end with a newline.

### 5. Keep reading until the server closes

s.recv(4096) returns up to 4096 bytes that have arrived so far. One call
may return only PART of the reply. (The practice server sends its answer
in two pieces on purpose.) When the server closes the connection, recv
returns b"" (empty bytes). So you read in a loop:

```
chunks = []
while True:
    piece = s.recv(4096)
    if piece == b"":
        break
    chunks.append(piece)
reply = b"".join(chunks)    # glue the pieces together
```

Then decode the reply. Use strip() to remove the newline at the end.
Then return it.

### 6. The protocol

A protocol is the agreed format of the conversation. Both sides follow
it. This protocol is:

- **client sends**: `READ <channel>\n`, for example `READ 7\n`
- **server sends**: one line of text. Then it closes the connection.

Send exactly this, in this order:

1. the word READ
2. one space
3. the channel number
4. a newline

## New words
- **server / client**: the server is the program that waits. The client is the program that connects.
- **localhost (127.0.0.1)**: your own computer, as a network address.
- **port**: a number that picks which program on a computer you talk to.
- **socket**: a program's end of a network connection.
- **TCP**: a reliable byte stream between two programs. Bytes arrive in order.
- **encode / decode**: encode converts text to bytes. decode converts bytes to text.
- **recv**: read the bytes that have arrived. This may be only part of the message.
- **protocol**: the agreed rules for what each side sends.
- **timeout**: how long to wait before you stop waiting.
- **tuple**: a fixed list in round brackets, like (host, port).
