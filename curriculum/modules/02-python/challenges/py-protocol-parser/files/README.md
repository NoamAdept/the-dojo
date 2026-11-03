# Parse Framed Protocol Bytes

What you will learn:

- how a stream of bytes is cut into messages ("frames") with a start
  marker and a length byte
- how an XOR checksum finds damaged data
- how to continue after bad data, so you do not lose any good message

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Goal
Complete parse_frames(data) in protocol.py.

## Frame shape

```
AA 55 | length | payload | XOR checksum
```

Return the payload bytes for each valid frame. Skip noise and bad frames.
Keep searching, so you still find the good frames that come later.

## Steps
1. Press Start and open protocol.py.
2. Write parse_frames. Then run `./check`.
3. Press Done when check passes.
