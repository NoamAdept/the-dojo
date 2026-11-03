## Parse Noisy Radio Frames

*py-protocol-parser · medium*

**Goal.** Complete `parse_frames(data)` in `protocol.py` so it finds every valid `AA 55 | length | payload | checksum` frame in a noisy byte stream and returns the payloads, skipping bad checksums and incomplete frames without losing later good frames.

**You need to know.**

- Bytes indexing (gives an int) versus slicing (gives bytes), and `data.find(pattern, start)` (README lesson 2).
- XOR checksums with `^` (README lesson 3, and pyz-bytes-hex task 7).
- A position variable and a `while` loop that moves forward (README lesson 5, and the `split_chunks` task in pyz-bytes-hex).
- Frame size is `2 + 1 + length + 1`.

**Walkthrough.**

1. Open `protocol.py`. Plan the loop: find a marker, read the length, check the frame fits, check the checksum, then jump past a good frame or move one byte on after a bad one.

2. Replace the `# TODO` and `return []` with:

   ```python
   def parse_frames(data):
       payloads = []
       i = 0
       while True:
           i = data.find(b"\xaa\x55", i)
           if i == -1:
               break
           if i + 2 >= len(data):
               break
           length = data[i + 2]
           end = i + 2 + 1 + length + 1
           if end > len(data):
               i += 1
               continue
           payload = data[i + 3:i + 3 + length]
           check = 0
           for b in payload:
               check ^= b
           if check == data[end - 1]:
               payloads.append(bytes(payload))
               i = end
           else:
               i += 1
       return payloads
   ```

   - `find` jumps straight to the next marker from position `i`, and `-1` means no more markers, so we stop.
   - `i + 2 >= len(data)` means the stream ends before the length byte, so there is nothing more to read.
   - `end` is one past the checksum byte; if it is beyond the data, this frame is incomplete, so step one byte and keep searching.
   - The payload starts after marker and length (`i + 3`), and the checksum is the last byte, `data[end - 1]`.
   - On a match, keep the payload and jump to `end`; on a mismatch, move only one byte, because a real marker could be hiding inside the "frame" we just rejected.

3. Try one valid frame by hand.

   ```bash
   python3 protocol.py aa5502484901
   ```

   It prints `4849`, the hex of the payload `HI` (`0x48 ^ 0x49` is `0x01`, the checksum).

4. Run the check.

   ```bash
   ./check
   ```

   The check builds `noise + good frame + junk + frame with a broken checksum + junk + good frame`, and expects exactly the two good payloads. It also expects `[]` for a frame missing its last byte.

**Check.** `./check` prints `CHECK_OK`. Press Done in the dojo to get the flag.

**Common mistakes.**

- Jumping past a bad frame (`i = end`) instead of one byte: harmless in this check, but it can swallow a real frame in real noise. Teach the one-byte step.
- Off by one in the offsets: payload at `i + 3`, checksum at `i + 3 + length`. Write the frame layout on paper first.
- Forgetting `i += 1` (or `i = end`) on some path, which gives an endless loop. If `./check` hangs, look for this.
