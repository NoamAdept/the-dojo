## Hex, Fixed-Size Types and Structs

*cpp-structs-hex · easy*

**Goal.** Fill in the nine small functions in `structs.cpp`: hex printing, `sizeof`, a struct with `.` and `->`, nibbles and bits, and rebuilding numbers from bytes in big- and little-endian order.

**You need to know.**

- `std::hex`, `std::setw`, `std::setfill`, `std::dec` (README, "Hexadecimal").
- `uint8_t`/`uint16_t`/`uint32_t` and `static_cast` (README, "Exact-size types").
- `.` on a struct, `->` on a pointer to a struct (README, "Plain structs, . and ->").
- `&` masks, `<<` and `>>` shifts, byte order (README, "Masks and shifts" and "Building a number from bytes").

**Walkthrough.**

Everything goes in `structs.cpp`. Delete each `// TODO task N` comment when you fill that part in. Do not edit `structs.hpp`.

1. Task 1, `print_byte`:

   ```cpp
   std::cout << "0x" << std::hex << std::setw(2) << std::setfill('0') << static_cast<int>(b) << std::dec << "\n";
   ```

   The cast stops `uint8_t` printing as a character, `setw(2)` plus `setfill('0')` gives `0a`, and `std::dec` puts `std::cout` back to decimal for later prints.

2. Task 2, `sample_bytes`:

   ```cpp
   return count * sizeof(uint16_t);
   ```

   Each `uint16_t` is 2 bytes, and `sizeof` keeps that right if the type changes.

3. Task 3, `make_reading`: keep the existing `reading r{};` and `return r;`, and fill the fields in between.

   ```cpp
   r.channel = channel;
   r.freq_hz = freq_hz;
   r.gain = gain;
   ```

4. Task 4, `retune`:

   ```cpp
   r->freq_hz = freq_hz;
   ```

   `r` is a pointer, so `->` reaches the field in the caller's struct and leaves the other fields alone.

5. Task 5, the three bit functions:

   ```cpp
   uint8_t low_nibble(uint8_t b)  { return b & 0x0f; }
   uint8_t high_nibble(uint8_t b) { return b >> 4; }
   bool bit_is_set(uint8_t flags, unsigned bit) { return ((flags >> bit) & 1u) != 0; }
   ```

   The mask `0x0f` keeps the right-hand 4 bits, `>> 4` moves the left-hand 4 bits down, and shifting the wanted bit to position 0 then masking with 1 tests it.

6. Task 6, `read_be16`:

   ```cpp
   return static_cast<uint16_t>((p[0] << 8) | p[1]);
   ```

   Big-endian means the first byte is the high one, so it moves up 8 bits.

7. Task 7, `read_le32`:

   ```cpp
   return static_cast<uint32_t>(p[0]) | (static_cast<uint32_t>(p[1]) << 8)
        | (static_cast<uint32_t>(p[2]) << 16) | (static_cast<uint32_t>(p[3]) << 24);
   ```

   Little-endian means the first byte is the lowest. Casting to `uint32_t` before shifting stops `0xc0 << 24` overflowing a signed `int`.

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Forgetting `std::dec`: task 1 fails on the line that should print `42`.
- Printing `b` without `static_cast<int>`: you get a strange character, not hex digits.
- Shifting `p[3] << 24` without the cast. The README says the sanitizer catches this, but with GCC in C++17 mode `./check` still passed in our test run. Insist on the casts anyway: `0xc0 << 24` does not fit in a signed `int`.
