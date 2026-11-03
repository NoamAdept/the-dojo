# Hex, Fixed-Size Types and Structs: lesson

### Hexadecimal

A **byte** is 8 bits. It holds a number from 0 to 255. Programmers usually write bytes in **hexadecimal** (base 16). Hex numbers start with the prefix `0x`.

Hex digits go from 0 to 9. Then `a`=10, `b`=11, and so on up to `f`=15. Each place is worth 16 times the place to its right:

```
0x0a = 10        0x10 = 16        0x2a = 2*16 + 10 = 42        0xff = 255
```

2 hex digits are always exactly 1 byte. Each single hex digit is 4 bits. 4 bits are called a **nibble**. In C++ you can write `0x2a` anywhere you can write `42`.

To print in hex, send `std::hex` to `std::cout`. These 2 settings come from `<iomanip>`:

- `std::setw(2)` asks for at least 2 characters.
- `std::setfill('0')` fills the empty places with zeros.

```cpp
std::cout << "0x" << std::hex << std::setw(2) << std::setfill('0') << 10 << "\n";   // 0x0a
std::cout << std::dec;     // back to normal decimal numbers
```

`std::setw` only changes the next value. But `std::hex` and `std::setfill` stay on. So when you finish, switch back with `std::dec`.

### Exact-size types: <cstdint>

A plain `int` can have different sizes on different computers. Bytes from files or radios need sizes that never change. `#include <cstdint>` gives you these types:

| type | bits | range |
|---|---|---|
| `uint8_t`  | 8  | 0 to 255 |
| `uint16_t` | 16 | 0 to 65535 |
| `uint32_t` | 32 | 0 to 4294967295 |

The `u` means **unsigned** (never negative).

There is one trap. `uint8_t` is really a `char` type underneath. So `std::cout << b` prints it as a letter, not a number. Change it to an `int` first with `static_cast<int>(b)`. This is called a **cast** (it changes a value to another type).

### sizeof

`sizeof(TYPE)` gives the size of a type in bytes, as a `std::size_t`. For example, `sizeof(uint32_t)` is 4. Use `sizeof` instead of typing the number. Then the code stays correct if the type changes.

### Plain structs, . and ->

In the Toolbox, your structs had member functions. A struct can also be plain data. Then it is a group of named **fields** (named values) and nothing else. `structs.hpp` has this struct:

```cpp
struct reading {
    uint16_t channel;
    uint32_t freq_hz;
    uint8_t gain;
};
```

- Use `.` on a struct variable.
- Use `->` on a **pointer** to a struct.

```cpp
reading r{};                   // {} sets every field to 0
r.channel = 3;                 // . on the struct itself
reading* p = &r;
p->freq_hz = 433920000;        // -> through a pointer; same as (*p).freq_hz
```

A function can return a whole struct, like any other value.

Remember this for later: `sizeof(reading)` is usually 12, not 2+4+1=7. The compiler adds hidden **padding** bytes (unused bytes). Then each field starts at an address that suits its size.

### Masks and shifts

`&` between 2 numbers is called bitwise AND. It keeps only the bits that are 1 in both numbers. The number you AND with is a **mask**. The mask says which bits to keep.

```
0x5c & 0x0f = 0x0c        (keep the low nibble: 0101 1100 & 0000 1111 = 0000 1100)
```

- `>>` shifts bits to the right. Bits that fall off the end are lost.
- `<<` shifts bits to the left. It adds zeros on the right.

A shift by 4 moves the number by 1 hex digit:

```
0x5c >> 4 = 0x05          0x05 << 4 = 0x50          1u << 3 = 0x08 (only bit 3 set)
```

Bits are numbered from 0, starting at the right. To ask "Is bit 3 set?", write `((flags >> 3) & 1) != 0`.

### Building a number from bytes

A 16-bit number needs 2 bytes. The **byte order** says which byte comes first:

- **big-endian**: the big (high) byte comes first. `0x1234` is stored as `12 34`.
- **little-endian**: the little (low) byte comes first. `0x1234` is stored as `34 12`.

Network protocols usually use big-endian. PCs and the Raspberry Pi use little-endian in their own memory.

To rebuild a number, shift each byte to its place. Then join the bytes with `|` (bitwise OR):

```cpp
const uint8_t b[2] = {0x12, 0x34};
uint16_t v = static_cast<uint16_t>((b[0] << 8) | b[1]);    // big-endian: v is 0x1234
```

Be careful with 32 bits. Before a shift, C++ turns a byte into a plain (signed) `int`. And `0x80 << 24` does not fit in an `int`. So convert the byte first: `static_cast<uint32_t>(b[3]) << 24`. If you forget, the checker's sanitizer reports the mistake.

### How this challenge works

Write your code in `structs.cpp`. `structs.hpp` is the header. It lists the functions so other files know they exist. Do not change it.

Each function has a `// TODO task N` comment. Delete the comment when you write the code. This tells `./check` that the task is started.

`./check` compiles your file together with a hidden test program. It uses `g++ -std=c++17 -Wall -Wextra -Werror` plus **sanitizers** (`-fsanitize=address,undefined`). Sanitizers are safety checks. They stop the program with a report at the moment it does one of these things:

- reads memory it should not
- follows a `nullptr`
- does arithmetic the C++ rules do not allow

Unused parameters are allowed here. So an unfinished task does not block the other tasks.

Do you want to try your functions yourself? Make a file `try.cpp` with `#include "structs.hpp"` and a `main`. Then run `g++ -std=c++17 -Wall -Wextra try.cpp structs.cpp -o try && ./try`.

### New words

- byte: 8 bits, a number from 0 to 255.
- hexadecimal (hex): base 16, written like `0x2a`, with digits 0-9 and a-f.
- nibble: 4 bits, one hex digit.
- unsigned: a type that cannot hold negative numbers.
- uint8_t / uint16_t / uint32_t: unsigned integers of exactly 8, 16 and 32 bits.
- cast: `static_cast<int>(b)`, which changes a value to another type.
- sizeof: the size of a type in bytes.
- field: one named value inside a struct.
- `->`: reaches a field through a pointer to a struct.
- padding: hidden unused bytes that the compiler may put inside a struct.
- mask: a number used with `&` to keep only some bits.
- shift (`<<`, `>>`): move bits left or right.
- big-endian / little-endian: high byte first / low byte first.

## Offline help

- Offline: `man ascii` has a table of every byte value in decimal and hex
