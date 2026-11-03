# Low-Level Data Manipulation

Write all your code in `tasks.h`. You can write inline, header-only code here. Each file in `tests/` checks one task. `./check` compiles them one at a time with `g++ -std=c++17`. So you can do the tasks in any order.

## C++ Low-Level Data Manipulation

Welcome to Module 12! This module uses bit manipulation, structs, and unions together. With them, you have full control over data in memory.

You often need this in embedded systems, network protocols, and very fast programs. There you often need to:
1.  Control single **bits** inside a byte.
2.  Know exactly how data sits in memory (**Padding** & **Alignment**).
3.  Read raw bytes as a different type (**Unions** & **Casts**).

Is this new to you? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

1. **RGB packer**: `uint32_t packRGB(uint8_t r, uint8_t g, uint8_t b)` returns `0x00RRGGBB`. Also write `unpackRGB(uint32_t, uint8_t& r, uint8_t& g, uint8_t& b)`.
2. **Toggle**: `template <class T> T toggleBit(T val, unsigned n)`.
3. **Protocol header**: a packed `struct Header { uint16_t id; uint8_t flags; uint8_t len; };`. It is 4 bytes. Add `static_assert(sizeof(Header) == 4)`.
4. **Power of two**: `bool isPowerOfTwo(int n)` uses `n & (n - 1)`. Zero and negative numbers are not powers of two.
5. **Packet header**:
   - Write a packed `struct PacketHeader { uint16_t id; uint8_t len; };` (3 bytes).
   - Write `PacketHeader readHeader(const uint8_t* raw)`. Use `reinterpret_cast`.
   - Assume a little-endian host, like a Raspberry Pi.
6. **Packet payload**: `std::string readPayload(const uint8_t* raw)` reads `len` characters after the header. Use pointer arithmetic to move past the header.
7. **Sensor variant**: write `using SensorValue = std::variant<int, double, std::string>;` and `std::string formatSensor(const SensorValue&)`. It returns one of:
   - `"count=12"`
   - `"volts=3.30"` (2 decimal places)
   - `"error: <msg>"`

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
