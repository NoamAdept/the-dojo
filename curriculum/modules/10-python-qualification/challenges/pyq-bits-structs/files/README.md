# Bit Manipulation and Structs



## Module 11: Bit Manipulation & Structs

Embedded systems, networking and drivers need low-level work with bits and bytes. Python usually hides this from you. But it gives you two strong tools for when you need it:

- bitwise operators
- the `struct` module

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

1. **Flag checker**: `bit_state(value, n)` returns `"ON"` or `"OFF"` for bit `n`. Bit numbers start at 0 (0-indexed). For example, in `0b1001_0110`, bit 4 is ON.
2. **Masking**: `clear_low_nibble(value)` sets the lowest 4 bits to 0 (it clears them).
3. **Struct packing**: `pack_reading(b, f, s)` packs 3 values into bytes: an unsigned byte, a float32 and a signed short. Use little-endian order and no padding. The `struct` format is `"<Bfh"`, and the result is 7 bytes.
4. **Endian swap**: `endian_bytes(value)` returns `(big_hex, little_hex)` for a 4-byte int. For example `0x12345678` gives `("12345678", "78563412")`.
5. **Bit counter**: `count_set_bits(n)` returns how many bits are 1 in an int that is 0 or more.
6. **Binary protocol parser**: `parse_packet(data)` takes a packet with this layout: `[header: 2 bytes big-endian 0xAA55][id: 1 byte][payload: uint32 big-endian]`. It returns `(id, payload)`. If the header is wrong or the length is wrong, it raises `ValueError`.
7. **BMP header reader**: `get_bmp_dimensions(path)` first checks that the file starts with `b"BM"` (at offset 0). If it does not, raise `ValueError`. Then it returns `(width, height)`. These are little-endian int32s at offsets 18 and 22. We give you a sample file, `pixel.bmp`.

## Check your work

Run `./check` as many times as you want. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
