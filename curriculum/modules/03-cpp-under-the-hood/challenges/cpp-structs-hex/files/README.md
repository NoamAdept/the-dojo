# Hex, Fixed-Size Types and Structs

**What you will learn:**

- how to write and print numbers in hex
- how to use exact-size integer types
- how to group values in a plain struct, and reach them through a pointer
- how to pick bits out of a byte
- how to build a number from bytes in either byte order

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

Fill in the functions in `structs.cpp`. Do not change `structs.hpp`.

1. **Hex printing**: `print_byte(b)` prints `b` as `0x` and exactly 2 lowercase hex digits, then a new line. `print_byte(10)` prints `0x0a`. After this, `std::cout` must print numbers in decimal again. So finish with `std::dec`.
2. **sizeof**: `sample_bytes(count)` returns how many bytes `count` samples of type `uint16_t` use. Use `sizeof`.
3. **Struct with `.`**: `make_reading(channel, freq_hz, gain)` returns a `reading` with those 3 fields filled in.
4. **Struct with `->`**: `retune(r, freq_hz)` changes the `freq_hz` field of the struct that `r` points at. It does not change the other fields.
5. **Masks and shifts**:
   - `low_nibble(0x5c)` returns `0x0c`.
   - `high_nibble(0x5c)` returns `0x05`.
   - `bit_is_set(flags, bit)` returns true when bit number `bit` is 1. Bit 0 is the rightmost bit.
6. **Big-endian**: `read_be16(p)` returns the 16-bit number stored big-endian in `p[0]`, `p[1]`. Bytes `12 34` give `0x1234`.
7. **Little-endian, 32 bits**: `read_le32(p)` returns the 32-bit number stored little-endian in `p[0]` to `p[3]`. Bytes `78 56 34 12` give `0x12345678`.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
