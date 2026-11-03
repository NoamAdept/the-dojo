## Decode a Header from Raw Bytes

*cpp-memory-layout · medium*

**Goal.** Write `decode_header` in `layout.cpp` so it refuses bad input and fills a `header` struct field by field from 6 raw bytes, with a little-endian `sequence`.

**You need to know.**

- The wire layout in the README: bytes 0-1 tag, 2-3 sequence (low byte first), 4 flags, 5 length.
- `->` to reach fields through `header* out`.
- Building a 16-bit number from two bytes with `<<` and `|` (from cpp-structs-hex).
- Why you must not cast `data` to a `header*`: padding and byte order (README lesson).

**Walkthrough.**

The whole answer is one function in `layout.cpp`. Delete each of the three `// TODO task N` lines as you do that part. Do not change `layout.hpp`.

1. Task 1: refuse bad input before touching anything.

   ```cpp
   if (data == nullptr || out == nullptr || size < 6) {
       return false;
   }
   ```

   This comes first so no byte is read and `*out` is not changed when the buffer is missing or too short.

2. Task 2: copy the single bytes and say it worked.

   ```cpp
   out->tag[0] = static_cast<char>(data[0]);
   out->tag[1] = static_cast<char>(data[1]);
   out->flags = data[4];
   out->length = data[5];
   return true;
   ```

   Each field comes from its own byte position, so struct padding never matters. The cast turns the byte into a letter for `tag`.

3. Task 3: build the sequence (put this before `return true;`).

   ```cpp
   out->sequence = static_cast<uint16_t>(data[2] | (data[3] << 8));
   ```

   Low byte first means `data[2]` stays where it is and `data[3]` moves up 8 bits. Bytes `34 12` give `0x1234` (4660).

4. The finished function:

   ```cpp
   bool decode_header(const uint8_t* data, std::size_t size, header* out)
   {
       if (data == nullptr || out == nullptr || size < 6) {
           return false;
       }
       out->tag[0] = static_cast<char>(data[0]);
       out->tag[1] = static_cast<char>(data[1]);
       out->sequence = static_cast<uint16_t>(data[2] | (data[3] << 8));
       out->flags = data[4];
       out->length = data[5];
       return true;
   }
   ```

**Check.** `./check` prints `3/3 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Writing `size <= 6` or `size < 5`: exactly 6 bytes is valid, 5 is not.
- Swapping the bytes for `sequence` (`data[2] << 8`): that is big-endian, and task 3 shows 13330 instead of 4660.
- Writing to `out` before the check (for example setting `out->flags = 0` first): the test expects the untouched value 77.
