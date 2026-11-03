# Inspect Memory

What you will learn:

- how to look at raw bytes in memory with GDB's x command
- how to read its output
- how to tidy hex bytes into a standard form

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Goal
Stop at inspect_packet. Examine 8 bytes, starting at packet.

## Deliverable
- **answer.txt**: lowercase hex bytes, no 0x, spaces between them (e.g. 41 42 ...)

## Steps
1. Press Start, then: `./run`
2. In GDB: break inspect_packet → run → x/8bx packet
3. Write answer.txt, then: `./check`
4. Press Done when check passes.
