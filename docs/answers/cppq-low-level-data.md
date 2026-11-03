## Low-Level Data Manipulation

*cppq-low-level-data · medium*

**Goal.** Pack and unpack bits, write packed structs that match a byte layout, read a header and payload out of a raw byte buffer, and format a `std::variant` sensor reading.

**You need to know.**

- Shifts and masks: `<<`, `>>`, `&`, `|`, `^` (README bit manipulation).
- `#pragma pack(push, 1)` removes padding; `static_assert(sizeof(...))` proves it.
- `reinterpret_cast` views bytes as a struct; pointer arithmetic skips past the header.
- `std::visit` with `if constexpr`, and `snprintf("%.2f")` for fixed decimals.

**Walkthrough.**

1. Run `./check`, then add `#include <cstdio>` and `#include <type_traits>` to the starter.

2. Task 1, RGB. Cast each byte up to 32 bits before shifting; masking with `0xFF` cuts one byte back out.

   ```cpp
   inline uint32_t packRGB(uint8_t r, uint8_t g, uint8_t b) {
       return (uint32_t(r) << 16) | (uint32_t(g) << 8) | uint32_t(b);
   }
   inline void unpackRGB(uint32_t c, uint8_t& r, uint8_t& g, uint8_t& b) {
       r = (c >> 16) & 0xFF;
       g = (c >> 8) & 0xFF;
       b = c & 0xFF;
   }
   ```

3. Task 2, toggle a bit. XOR with a single 1-bit flips just that bit. `T(1)` makes the shift happen in the right width (bit 31 of a `uint32_t`).

   ```cpp
   template <class T>
   T toggleBit(T val, unsigned n) { return static_cast<T>(val ^ (T(1) << n)); }
   ```

4. Tasks 3 and 5, packed structs. Without packing, `PacketHeader` would be padded to 4 bytes. Put both structs inside one `push`/`pop` pair.

   ```cpp
   #pragma pack(push, 1)
   struct Header { uint16_t id; uint8_t flags; uint8_t len; };
   struct PacketHeader { uint16_t id; uint8_t len; };
   #pragma pack(pop)
   static_assert(sizeof(Header) == 4);
   ```

5. Task 4, power of two. A power of two has exactly one bit set, so `n & (n - 1)` clears it to 0. Check `n > 0` first.

   ```cpp
   inline bool isPowerOfTwo(int n) { return n > 0 && (n & (n - 1)) == 0; }
   ```

6. Task 5, read the header. On a little-endian Pi the bytes `01 00` read as id 1.

   ```cpp
   inline PacketHeader readHeader(const uint8_t* raw) { return *reinterpret_cast<const PacketHeader*>(raw); }
   ```

7. Task 6, payload. The text starts `sizeof(PacketHeader)` (3) bytes in, and is `len` bytes long. The test buffer has an extra `!` after `HELLO` that must not be read.

   ```cpp
   inline std::string readPayload(const uint8_t* raw) {
       const PacketHeader* h = reinterpret_cast<const PacketHeader*>(raw);
       const char* data = reinterpret_cast<const char*>(raw + sizeof(PacketHeader));
       return std::string(data, data + h->len);
   }
   ```

8. Task 7, sensor variant. One branch per type; `%.2f` gives exactly two decimals (`3.30`).

   ```cpp
   using SensorValue = std::variant<int, double, std::string>;

   inline std::string formatSensor(const SensorValue& v) {
       return std::visit([](const auto& x) -> std::string {
           using T = std::decay_t<decltype(x)>;
           if constexpr (std::is_same_v<T, int>) {
               return "count=" + std::to_string(x);
           } else if constexpr (std::is_same_v<T, double>) {
               char buf[32];
               std::snprintf(buf, sizeof buf, "volts=%.2f", x);
               return buf;
           } else {
               return "error: " + x;
           }
       }, v);
   }
   ```

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Forgetting `#pragma pack(pop)`: every struct after it stays packed, which can break other code.
- Shifting a `uint8_t` by 16 without casting, or writing `1 << n` instead of `T(1) << n`.
- Using `std::string(data)` for the payload: it reads until a zero byte and picks up the trailing `!`.
