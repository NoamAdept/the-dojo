# Low-Level Data Manipulation: lesson

### 1. Bitwise Operators

These operators work on the binary form of integers (the 0s and 1s). They look at each bit on its own.

| Operator | Name | Description |
|---|---|---|
| `&` | AND | 1 if *both* bits are 1 |
| `|` | OR | 1 if *at least one* bit is 1 |
| `^` | XOR | 1 if the 2 bits are *different* |
| `~` | NOT | Flip all bits (0->1, 1->0) |
| `<<` | Left Shift | Move bits to the left (multiply by 2) |
| `>>` | Right Shift | Move bits to the right (divide by 2) |

```cpp
#include <iostream>
#include <bitset>

// Helper to print binary
void printBin(int n) {
    std::cout << n << " : " << std::bitset<8>(n) << std::endl;
}

int main() {
    int a = 5;  // 00000101
    int b = 3;  // 00000011
    
    std::cout << "a & b: "; 
    printBin(a & b); // 001
    
    std::cout << "a | b: ";
    printBin(a | b); // 111
    
    std::cout << "a ^ b: ";
    printBin(a ^ b); // 110
    
    return 0;
}
```

### 2. Masks and Standard Bit Operations

A **Mask** is a value that you use to pick out certain bits.

In these examples, `reg` is your variable and `n` is the bit position. Bit positions start at 0 (0-indexed).

1.  **Set a bit** (make it 1): `reg |= (1 << n);`
2.  **Clear a bit** (make it 0): `reg &= ~(1 << n);`
3.  **Toggle a bit** (flip it): `reg ^= (1 << n);`
4.  **Check a bit**: `if (reg & (1 << n)) ...`

```cpp
#include <iostream>
#include <bitset>

int main() {
    unsigned char reg = 0; // 00000000
    
    // Set bit 2
    reg |= (1 << 2); 
    std::cout << "Set 2:    " << std::bitset<8>(reg) << std::endl;
    
    // Clear bit 2
    reg &= ~(1 << 2);
    std::cout << "Clear 2:  " << std::bitset<8>(reg) << std::endl;
    
    // Toggle bit 0
    reg ^= (1 << 0);
    std::cout << "Toggle 0: " << std::bitset<8>(reg) << std::endl;
    
    return 0;
}
```

### 3. Struct Layout and Padding

Now we move up from bits to bytes. You might think that `sizeof(struct)` is the sum of the sizes of its members. **Often it is not.**

CPUs like to read data at aligned addresses. For example, they like integers to start at an address that is a multiple of 4. So the compiler adds empty **Padding Bytes** between members to make this true.

```cpp
#include <iostream>

struct Padded {
    char a;  // 1 byte
    int b;   // 4 bytes
    char c;  // 1 byte
};

int main() {
    std::cout << "Size of Padded: " << sizeof(Padded) << std::endl;
    // Expected: 12 bytes (not 6!)
    // Layout: [a][pad][pad][pad] [b b b b] [c][pad][pad][pad]
    return 0;
}
```

### 4. Packed Structures and Bitfields

Sometimes you need exact control of the layout, for example for network protocols or to save memory. You can do this in 2 ways:

1. **Attributes**: `__attribute__((packed))` (GCC/Clang) removes the padding.
2. **Bitfields**: give a struct member an exact width in bits.

```cpp
#include <iostream>

struct __attribute__((packed)) Packed {
    char a;
    int b;
    char c;
};

struct PackedDate {
    unsigned int day   : 5; // 0-31 fits in 5 bits
    unsigned int month : 4; // 0-15 fits in 4 bits
    unsigned int year  : 7; // 0-127
};

int main() {
    std::cout << "Size of Packed: " << sizeof(Packed) << std::endl; // 6 bytes
    std::cout << "Size of Bitfield: " << sizeof(PackedDate) << std::endl; // 4 bytes (typically)
    return 0;
}
```

### 5. Unions

In a `union`, all members share the **same memory location**. Only 1 member is valid at a time.

Embedded systems often use unions for "Type Punning". This means you look at the raw bytes of a larger type. Unions are also used for "Variant" types (a value that can be one of several types).

```cpp
#include <iostream>

union Converter {
    uint32_t val;
    uint8_t bytes[4];
};

int main() {
    Converter c;
    c.val = 0xAABBCCDD;
    
    // Little Endian machines (x86, ARM) store LSB first
    std::cout << std::hex;
    std::cout << "Byte 0: " << (int)c.bytes[0] << std::endl; // DD
    std::cout << "Byte 3: " << (int)c.bytes[3] << std::endl; // AA
    return 0;
}
```

### 6. Endianness

Endianness is the order of the bytes inside a number that uses more than 1 byte. Different CPUs store these numbers in a different order.

- **Little Endian** (Intel/ARM): the Least Significant Byte (the smallest part) comes first.
- **Big Endian** (Network): the Most Significant Byte (the largest part) comes first.

### 7. `std::variant` (Modern C++)

Unions are unsafe. You do not know *which* member is valid right now.

C++17 adds `std::variant`. It is a type-safe union. It remembers which type is active (valid) right now.

```cpp
#include <iostream>
#include <variant>

int main() {
    std::variant<int, float> v;
    
    v = 10;
    if (std::holds_alternative<int>(v)) {
        std::cout << "Value: " << std::get<int>(v) << std::endl;
    }
    return 0;
}
```

---

## New words

- **bit**: a single 0 or 1.
- **mask**: a value that picks out some bits.
- **padding**: empty bytes the compiler adds inside a struct.
- **alignment**: the rule that some data must start at an address that is a multiple of a number (for example 4).
- **packed struct**: a struct with no padding.
- **union**: a type where all members share the same memory.
- **endianness**: the order of bytes inside a number.
