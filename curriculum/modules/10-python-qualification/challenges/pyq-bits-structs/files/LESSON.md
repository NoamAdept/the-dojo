# Bit Manipulation and Structs: lesson

### 1. Bitwise Operators

A bitwise operator works on each bit (each 0 or 1) of a number. Python has the same bitwise operators as C:

- `&` (AND)
- `|` (OR)
- `^` (XOR)
- `~` (NOT)
- `<<` (Left Shift)
- `>>` (Right Shift)

**Important difference from C**: Python integers have arbitrary precision. This means they can have as many bits as they need ("infinite bits"). This changes how bitwise NOT (`~`) and shifts behave.

```python
x = 0b1010  # 10
y = 0b1100  # 12

print(f"AND: {bin(x & y)}")
print(f"OR:  {bin(x | y)}")
print(f"XOR: {bin(x ^ y)}")

# NOT: In Python ~x is -(x+1) because of infinite 2's complement
print(f"NOT: {bin(~x)} (Decimal: {~x})") 

# To simulate 8-bit behavior, mask it:
print(f"8-bit NOT: {bin(~x & 0xFF)}")
```

### 2. Setting, Clearing, and Toggling Bits

A flag register is a number where each bit is an on/off switch. Use these common patterns to change one bit:

- Set bit N: `x | (1 << N)`
- Clear bit N: `x & ~(1 << N)`
- Toggle bit N: `x ^ (1 << N)`
- Check bit N: `(x >> N) & 1`

```python
flags = 0b0000_1000  # Initial state

# Set bit 0
flags |= (1 << 0)
print(f"Set bit 0:   {bin(flags)}")

# Clear bit 3
flags &= ~(1 << 3)
print(f"Clear bit 3: {bin(flags)}")

# Toggle bit 1
flags ^= (1 << 1)
print(f"Toggle bit 1:{bin(flags)}")
```

### 3. The `struct` Module

C code and binary files store data in a fixed layout. A C struct is a group of values, and each value has a fixed size in bytes. To talk to C code or read binary files, you must pack Python values into this layout. The `struct` module does this.

You describe the layout with a format string. Each letter is one value:
- `i`: int (4 bytes)
- `f`: float (4 bytes)
- `d`: double (8 bytes)
- `c`: char (1 byte)
- `B`: unsigned char (1 byte)

```python
import struct

# Pack an int (4 bytes) and a short (2 bytes)
# 'h' is short, 'i' is int
binary_data = struct.pack("ih", 1000, 50)
print(f"Packed: {binary_data} (Len: {len(binary_data)}) ")
```

### 4. Byte Order (Endianness)

Endianness is the order of the bytes in a number that is bigger than 1 byte. Little-endian puts the smallest byte first. Big-endian puts the biggest byte first.

You **must** give the endianness, so your code works the same on every machine (portability). Put one of these characters at the start of the format string:

- `<`: Little-endian (the Intel/AMD standard)
- `>`: Big-endian (the network standard)
- `!`: Network standard (Big-endian)

```python
val = 0x12345678

big_endian = struct.pack(">I", val)
little_endian = struct.pack("<I", val)

print(f"Big:    {big_endian.hex()}")    # 12 34 56 78
print(f"Little: {little_endian.hex()}") # 78 56 34 12
```

### 5. Unpacking Data

`struct.unpack` does the opposite of `pack`. It turns binary data back into Python values. It returns them in a tuple.

```python
data = b'\x01\x00\x00\x00\x00?\x00\x00' # Binary blob

# Unpack as Little Endian Int + Float
unpacked = struct.unpack("<If", data)
print(f"Unpacked: {unpacked}") # 1, 0.5
```

### 6. `bytearray` vs `bytes`

- `bytes`: An immutable sequence of bytes. You cannot change it after you create it.
- `bytearray`: A mutable sequence of bytes. You can change, add or remove bytes.

```python
b = bytearray(b"Hello")
b[0] = ord('J')
print(f"Modified: {b}")

# Appending bytes
b.extend(b" World")
print(f"Extended: {b}")
```

### 7. `int.from_bytes` and `to_bytes`

These methods give you a clearer way to turn raw bytes into integers, and integers into bytes. You do not need `struct` for this.

```python
num = 1024
b_data = num.to_bytes(4, byteorder='big')
print(f"Bytes: {b_data.hex()}")

recovered = int.from_bytes(b_data, byteorder='big')
print(f"Recovered: {recovered}")
```

### 8. Working with Hex Literals

A literal is a value that you write directly in your code. Python supports:

- hex literals (`0xFF`)
- octal literals (`0o77`)
- binary literals (`0b11`)

To show a number in one of these forms, use format strings (f-strings).

```python
x = 255
print(f"Hex: {hex(x)}")
print(f"Bin: {bin(x)}")

# Output formatting
print(f"Padded Hex: 0x{x:04X}")
print(f"Padded Bin: 0b{x:08b}")
```

---

## New words

- **bit**: one binary digit, 0 or 1.
- **mask**: a number you use with `&`, `|` or `^` to pick or change some bits.
- **nibble**: 4 bits (half a byte).
- **flag register**: a number where each bit means "on" or "off" for one thing.
- **struct**: a fixed layout of values in bytes, like a C struct.
- **endianness**: the order of the bytes in a multi-byte number.
- **padding**: extra empty bytes that C may add between values. `<` and `>` turn it off.
