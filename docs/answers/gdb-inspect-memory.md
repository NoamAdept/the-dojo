## Inspect Bytes in Memory

*gdb-inspect-memory · medium*

**Goal.** At `inspect_packet`, examine the 8 bytes the `packet` pointer points at, and write them to `answer.txt` as lowercase two-digit hex separated by spaces, without `0x`.

**You need to know.**

- GDB's `x` command examines raw memory (README.txt lesson).
- The format `/8bx` means 8 units, `b` = one byte each, `x` = hex.
- The address at the start of the output line is not part of the answer.
- `print` on a byte pointer shows a string, which is why `x` is the right tool here.

**Walkthrough.**

1. Build.

   ```bash
   ./run
   ```

2. Stop at the function and examine the bytes.

   ```text
   gdb ./target
   (gdb) break inspect_packet
   (gdb) run
   Breakpoint 1, inspect_packet (packet=0x7fff... "\252U\003\020") at target.cpp:5
   (gdb) x/8bx packet
   0x7fff...:  0xaa  0x55  0x03  0x10  0x00  0xfe  0x01  0xef
   (gdb) quit
   ```

   The stop line shows `packet` as a strange string because GDB treats a byte pointer as text. `x/8bx` shows the real bytes. The address before the colon changes every run; ignore it.

3. Normalize: drop each `0x`, keep two digits and lowercase, one space between. This matches the array in `target.cpp`: `{0xaa, 0x55, 0x03, 0x10, 0x00, 0xfe, 0x01, 0xef}`.

4. Write the answer and check.

   ```bash
   echo 'aa 55 03 10 00 fe 01 ef' > answer.txt
   ./check
   ```

**Check.** `./check` prints `CHECK_OK`. Then press Done.

**Common mistakes.**

- Copying the address (`0x7fff...:`) as if it were a byte.
- Writing `3` or `0` instead of `03` and `00`: every byte needs two digits.
- Using `x/8x packet` without `b`: GDB may show bigger units (words), and the byte order then looks reversed.
