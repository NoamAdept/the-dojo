## Bit Manipulation and Structs

*pyq-bits-structs · medium*

**Goal.** Read and change bits with shifts and masks, pack and unpack binary data with `struct`, parse a tiny binary protocol and read the width and height out of a BMP header.

**You need to know.**

- `>>`, `&`, `~` and hex/binary literals.
- `struct.pack`, `struct.unpack`, `struct.unpack_from`, and format codes `B`, `h`, `H`, `I`, `i`, `f`.
- `<` means little-endian with no padding, `>` means big-endian.
- `int.to_bytes(n, "big" | "little")` and `bytes.hex()`.

**Walkthrough.**

1. Run `./check`. For task 7, make the sample image yourself (the README says it is provided, but the workspace ships the script that writes it).

   ```bash
   ./check
   python3 make_bmp.py      # writes pixel.bmp, a 3x2 image
   ```

2. Task 1. Shift bit `n` down to position 0 and mask it with `1`.

   ```python
   def bit_state(value, n):
       return "ON" if (value >> n) & 1 else "OFF"
   ```

3. Task 2. `~0xF` has every bit set except the low four, so `&` clears just those.

   ```python
   def clear_low_nibble(value):
       return value & ~0xF
   ```

4. Task 3. `<` removes padding, so the result is 1 + 4 + 2 = 7 bytes.

   ```python
   def pack_reading(b, f, s):
       return struct.pack("<Bfh", b, f, s)
   ```

5. Task 4. The same int written in both byte orders, shown as hex text.

   ```python
   def endian_bytes(value):
       return value.to_bytes(4, "big").hex(), value.to_bytes(4, "little").hex()
   ```

6. Task 5. `bin()` gives a string like `"0b1011"`; counting `"1"` works for any size int (the check uses `2**64 - 1`).

   ```python
   def count_set_bits(n):
       return bin(n).count("1")
   ```

7. Task 6. Check the length first, because `struct.unpack` raises `struct.error` (not `ValueError`) on the wrong size. `>HBI` is a big-endian uint16, uint8, uint32.

   ```python
   def parse_packet(data):
       if len(data) != 7:
           raise ValueError(f"expected 7 bytes, got {len(data)}")
       header, pid, payload = struct.unpack(">HBI", data)
       if header != 0xAA55:
           raise ValueError(f"bad header {header:#06x}")
       return pid, payload
   ```

8. Task 7. Read the first 26 bytes, check the `BM` magic, then read two little-endian int32s starting at offset 18.

   ```python
   def get_bmp_dimensions(path):
       with open(path, "rb") as fh:
           head = fh.read(26)
       if head[:2] != b"BM":
           raise ValueError("not a BMP file")
       return struct.unpack_from("<ii", head, 18)
   ```

   Try it by hand: `python3 -c "import tasks; print(tasks.get_bmp_dimensions('pixel.bmp'))"` prints `(3, 2)`.

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`. Press Done for the flag.

**Common mistakes.**

- Using `"Bfh"` without `<`: native alignment pads the float to a 4-byte boundary and the result is 10 bytes, not 7.
- Not checking the length in `parse_packet`, so a short packet raises `struct.error` and the check fails.
- Opening the BMP in text mode, or using `>ii` (big-endian) for the dimensions.
