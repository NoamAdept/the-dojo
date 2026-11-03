# Decode a Header from Raw Bytes: lesson

### A buffer of bytes

Files, radios and network cards give your program a **buffer**. A buffer is a block of bytes in memory. Low-level C++ passes it as 2 things: a pointer to the first byte, and its size:

```cpp
bool decode_header(const uint8_t* data, std::size_t size, header* out);
```

`data[0]` is the first byte. `data[size - 1]` is the last byte. Anything after that is not yours to read.

### Letters are bytes too

Text is stored as numbers. The numbers come from the **ASCII** table. For example:

- `'R'` is the byte `0x52`.
- `'X'` is `0x58`.
- `'0'` is `0x30`.

When you store a byte in a `char`, you get that letter. So `char c = static_cast<char>(0x52);` is `'R'`.

### The header

A header is the first part of a message. It describes the rest of the message. The 6 bytes of this header arrive in this order:

```
byte:   0        1        2              3               4       5
        tag[0]   tag[1]   sequence low   sequence high   flags   length
```

For example, `52 58 34 12 a5 09` means:

- tag `RX`
- sequence `0x1234`
- flags `0xa5`
- length 9

The sequence is **little-endian**. This means the low byte comes first. So you rebuild it as `data[2] | (data[3] << 8)`. You did the same in the last challenge.

### Your computer's own byte order

Numbers in your program's memory are bytes too. You can look at the bytes of any variable through a `const uint8_t*`. `reinterpret_cast` is the cast that says "treat this address as a different kind of pointer":

```cpp
uint16_t v = 0x1234;
const uint8_t* bytes = reinterpret_cast<const uint8_t*>(&v);
std::cout << std::hex << static_cast<int>(bytes[0]) << " " << static_cast<int>(bytes[1]) << "\n";
// prints "34 12" on a Raspberry Pi or a PC: they are little-endian inside
```

### Why not cast the bytes to a struct?

`layout.hpp` has a `struct header` with the same fields. You may want to write `reinterpret_cast<const header*>(data)` and stop there. Do not do this. There are 3 reasons:

- The compiler may put hidden **padding** (unused bytes) between fields. Then the struct's bytes may not match the message's bytes. For example, `struct odd { uint8_t a; uint32_t b; };` has `sizeof(odd) == 8`, not 5. There are 3 padding bytes after `a`.
- A big-endian computer would read the sequence in the wrong order.
- The C++ rules do not allow you to read a `uint8_t` buffer as a different struct type. This is **undefined behaviour**: the program may do anything.

Instead, read byte by byte and build each field yourself. This works the same on every computer.

### Refuse bad input first

Before you read `data[5]`, you must know that `size` is at least 6. You must also refuse a `nullptr`. Never follow it. So check first and return `false`. Only read the bytes after the check.

### How this challenge works

Write your code in `layout.cpp`. `layout.hpp` is the header. It lists the functions so other files know they exist. Do not change it.

Each function has a `// TODO task N` comment. Delete the comment when you write the code. This tells `./check` that the task is started.

`./check` compiles your file together with a hidden test program. It uses `g++ -std=c++17 -Wall -Wextra -Werror` plus **sanitizers** (`-fsanitize=address,undefined`). Sanitizers are safety checks. They stop the program with a report at the moment it does one of these things:

- reads memory it should not
- follows a `nullptr`
- does arithmetic the C++ rules do not allow

Unused parameters are allowed here. So an unfinished task does not block the other tasks.

Do you want to try your functions yourself? Make a file `try.cpp` with `#include "layout.hpp"` and a `main`. Then run `g++ -std=c++17 -Wall -Wextra try.cpp layout.cpp -o try && ./try`.

### New words

- buffer: a block of bytes in memory, passed as a pointer plus a size.
- ASCII: the standard numbering of letters and digits as bytes (`'R'` = `0x52`).
- header: the first part of a message, which describes the rest.
- little-endian: low byte stored first.
- `reinterpret_cast`: treats an address as a different kind of pointer.
- padding: unused bytes that a compiler may put inside a struct.
- undefined behaviour: something the C++ rules forbid. If it happens, the program may do anything.

## Offline help

- Offline: `man ascii` (table of byte values for letters)
