# Bytes, Hex and Binary

**What you will learn:**

- how Python holds raw data as **bytes**,
- how to read and write numbers in hex and binary,
- how to take numbers out of a byte buffer (a block of bytes), one field at a time.

To try the examples, type `python3`. You get the `>>>` prompt. Type the examples line by line. `exit()` leaves.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

Replace each `raise NotImplementedError` in `tasks.py`.

1. **Hex and binary**:
   - `to_hex(n)` returns `hex(n)`.
   - `from_hex(text)` turns hex text such as `"ff"` or `"0x1a"` into an int.
   - `to_binary(n)` returns the binary digits **without** the `0b`: `to_binary(5)` returns `"101"`.
2. **str and bytes**: `text_to_bytes(text)` returns the text as bytes. `bytes_to_text(data)` turns bytes back into a str.
3. **Hex text and bytes**: `parse_hex(text)` turns hex text like `"48 69 21"` into bytes. `show_hex(data)` turns bytes into hex text like `"486921"`.
4. **Bytes are ints**: `byte_values(data)` returns a list of the ints in `data`. `last_byte(data)` returns the last byte as an int.
5. **Two-byte numbers**: `read_u16(data, pos)` returns the unsigned little-endian 16-bit number that starts at index `pos`. `read_i16(data, pos)` returns the signed one. Use `int.from_bytes`.
6. **struct**: `read_u16_struct(data, pos)` returns the same number as `read_u16`. But here, use `struct.unpack("<H", ...)`.
7. **Checksum**: `xor_checksum(data)` returns the XOR of all the bytes. For empty data it returns 0.
8. **Walk a buffer**: `split_chunks(data)` reads a buffer made of chunks. Each chunk is 1 length byte, then that many bytes. Return a list of the chunk contents as bytes. For example, `split_chunks(b"\x02hi\x03abc")` returns `[b"hi", b"abc"]`. Sometimes a chunk says it has more bytes than are left. Then `raise ValueError`.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
