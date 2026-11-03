## Bytes, Hex and Binary

*pyz-bytes-hex · easy*

**Goal.** Fill in thirteen small functions in `tasks.py` that convert between ints, hex, binary, text and bytes, read 16-bit numbers, compute an XOR checksum, and walk a length-prefixed buffer.

**You need to know.**

- `hex`, `bin`, `int(text, 16)`; `str.encode()` and `bytes.decode()` (README lesson).
- `bytes.fromhex`, `bytes.hex()`, and that indexing bytes gives an int while slicing gives bytes.
- Little-endian 16-bit numbers with `int.from_bytes` and `struct.unpack("<H", ...)`.
- XOR (`^`) and a `while` loop with a moving position.

**Walkthrough.**

1. Task 1: hex and binary, one call each.

   ```python
   def to_hex(n):
       return hex(n)

   def from_hex(text):
       return int(text, 16)

   def to_binary(n):
       return bin(n)[2:]
   ```

   `int(text, 16)` reads base 16 and accepts both `"ff"` and `"0x1a"`; `[2:]` slices the `0b` off the front of `bin`.

2. Task 2: str and bytes.

   ```python
   def text_to_bytes(text):
       return text.encode()

   def bytes_to_text(data):
       return data.decode()
   ```

   `encode` turns characters into bytes (UTF-8), `decode` goes back.

3. Task 3: hex text and bytes.

   ```python
   def parse_hex(text):
       return bytes.fromhex(text)

   def show_hex(data):
       return data.hex()
   ```

   `fromhex` ignores the spaces in `"48 69 21"`; `.hex()` writes two lower-case digits per byte with no spaces.

4. Task 4: bytes are ints.

   ```python
   def byte_values(data):
       return list(data)

   def last_byte(data):
       return data[-1]
   ```

   Looping over bytes (which `list` does) gives ints 0 to 255, and a single index also gives an int.

5. Task 5: two-byte numbers.

   ```python
   def read_u16(data, pos):
       return int.from_bytes(data[pos:pos + 2], "little")

   def read_i16(data, pos):
       return int.from_bytes(data[pos:pos + 2], "little", signed=True)
   ```

   Slice exactly the two bytes first; `"little"` means the low byte comes first, and `signed=True` makes `ff ff` read as -1.

6. Task 6: the same with struct (already imported at the top).

   ```python
   def read_u16_struct(data, pos):
       return struct.unpack("<H", data[pos:pos + 2])[0]
   ```

   `<` is little-endian, `H` is unsigned 16-bit, and `unpack` always returns a tuple, so take `[0]`.

7. Task 7: XOR checksum.

   ```python
   def xor_checksum(data):
       check = 0
       for b in data:
           check ^= b
       return check
   ```

   Start at 0 (so empty data gives 0) and XOR each byte in.

8. Task 8: walk the buffer.

   ```python
   def split_chunks(data):
       chunks = []
       pos = 0
       while pos < len(data):
           length = data[pos]
           start = pos + 1
           if start + length > len(data):
               raise ValueError("chunk runs past the end")
           chunks.append(data[start:start + length])
           pos = start + length
       return chunks
   ```

   Read the length byte, check the chunk fits, take the slice, then jump past it. A length of 0 gives an empty `b""` chunk, which is correct.

9. Run the check.

   ```bash
   ./check
   ```

**Check.** `./check` prints `8/8 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- `data[-1:]` instead of `data[-1]` in `last_byte`: a slice is bytes, not an int.
- Passing the whole buffer to `struct.unpack` instead of a 2-byte slice: it raises `struct.error`.
- In `split_chunks`, forgetting the size check (a slice past the end silently returns fewer bytes, so no error is raised), or forgetting to add the 1 for the length byte.
