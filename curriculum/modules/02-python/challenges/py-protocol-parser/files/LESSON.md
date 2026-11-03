# Parse Framed Protocol Bytes: lesson

### 1. Frames in a byte stream

A radio link delivers one long run of bytes. Some of the bytes are noise.
Each message inside the bytes is wrapped in a frame. The frame helps the
receiver find the message:

```
AA 55 | length | payload ...       | checksum
2 B   | 1 B    | "length" bytes    | 1 B
```

- AA 55 (hex, two bytes) is the marker. It means "a frame may start here".
- The length byte says how many payload bytes come next.
- The payload is the real message.

So a whole frame is 2 + 1 + length + 1 bytes.

### 2. Working with bytes (see the binary-decoder lesson for what a byte is)

```
data = b"xx\xaa\x55\x02HI\x01"
data[2]             # 170 (indexing one byte gives a number)
data[3:5]           # b'U\x02' (slicing gives bytes)
data.find(b"\xaa\x55", 0)   # 2: position of the marker, or -1
```

`find(pattern, start)` searches from position `start`. Use it to look for
the NEXT marker after the one you just handled.
bytes([72, 73]) builds bytes from numbers. It equals b"HI".

### 3. XOR and checksums

XOR (written ^ in Python) compares two numbers bit by bit. The result
bit is 1 where the bits are different. It is 0 where they are the same.
For example, 0x48 ^ 0x49 is 0x01.

A checksum is a small number. The sender calculates it from the payload.
The receiver calculates it again. If the two numbers are different, the
frame was damaged. The receiver must throw it away. Here the checksum is
all payload bytes XORed together:

```
c = 0
for b in payload:
    c = c ^ b
```

### 4. Never trust the input

Here are things that can go wrong. In each case, skip the frame:

- The marker is there, but the stream ends before the length byte.
- The length says more bytes than are left. The frame is incomplete.
- The checksum does not match.

### 5. Resynchronising

Resynchronising means finding the next real frame after an error. Use a
position variable `i` and a while loop.

- After a GOOD frame, move `i` past the whole frame.
- After a BAD frame, move `i` forward by only one byte. Then search again.

Why only one byte? The "bad frame" might really be noise that contained
AA 55 by chance. A real marker could be a few bytes later. It could be
inside the bytes that you wrongly thought were a frame.

You can try your function from the command line with a hex string. This
example is one valid frame that carries "HI". Type the hex as one word,
with no spaces:

```
$ python3 protocol.py aa5502484901
4849
```

It prints the payload in hex.

## New words
- **frame**: one message plus the extra bytes that mark and protect it.
- **marker (sync word)**: fixed bytes that signal the start of a frame.
- **payload**: the useful message inside a frame.
- **length field**: a byte that says how long the payload is.
- **XOR (^)**: a bit-by-bit test for "different?". The result is 1 where two bits are different.
- **checksum**: a small value calculated from data. It shows if the data was damaged.
- **resynchronise**: find the next real frame after noise or errors.
- **stream**: data that arrives as one continuous run of bytes.
