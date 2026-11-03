# Bytes, Hex and Binary: lesson

### Hex and binary: other ways to write a number

A computer stores everything as **bits**. A bit is a 0 or a 1. Eight bits make one **byte**. One byte holds a
whole number from 0 to 255. Normal decimal numbers are not easy to use for bytes. So programmers use two other
ways to write the **same** numbers:

- **binary** (base 2). You write `0b` in front: `0b101` is 5 (one 4, no 2, one 1).
- **hexadecimal** or **hex** (base 16). You write `0x` in front. Its digits are `0`-`9`, then `a`-`f`
  for 10 to 15. `0xff` is 15*16 + 15 = 255. This is the biggest byte. One byte is always exactly 2 hex digits.

```python
print(0xff, 0b101)      # 255 5        Python reads both forms as normal ints
print(hex(255))         # 0xff         int -> hex text
print(bin(5))           # 0b101        int -> binary text
print(int("ff", 16))    # 255          hex text -> int (16 means "base 16")
print(int("0x1a", 16))  # 26           the 0x in front is allowed too
print(int("101", 2))    # 5            binary text -> int
```

`hex()` and `bin()` give back **text** (a str). They do not give back a number.

### bytes vs str

A **str** is text: letters. A **bytes** value is a row of raw numbers. Each number is 0 to 255. This is what
you really get from a file, a network socket or a radio. A bytes literal (a bytes value written in your code)
looks like a string with `b` in front:

```python
data = b"Hi!"
print(type(data))       # <class 'bytes'>
print("Hi!".encode())   # b'Hi!'       str -> bytes
print(b"Hi!".decode())  # Hi!          bytes -> str
print(bytes([72, 105])) # b'Hi'        a list of numbers -> bytes
```

Some bytes are not printable letters. Python shows them as `\x` and 2 hex digits. For example, `b"\x00\xff"`
is the 2 bytes 0 and 255. To read a whole binary file as bytes, open it with `"rb"` (read binary):
`data = open("samples.bin", "rb").read()`.

### Hex text and bytes

People often write data down as hex text, with 2 digits for each byte. Two methods convert in both
directions:

```python
print(bytes.fromhex("48 69 21"))   # b'Hi!'      spaces are allowed
print(b"Hi!".hex())                # 486921
```

### Indexing bytes gives ints

Here bytes are different from str. One item of a bytes value is an **int**. It is not a one-letter string.
A slice (a part of the bytes, like `data[0:2]`) is still bytes:

```python
data = b"Hi!"
print(data[0])          # 72           an int (the code for "H")
print(list(data))       # [72, 105, 33]
print(data[0:2])        # b'Hi'        a slice is bytes
```

### Numbers bigger than one byte

A number up to 65535 needs **two** bytes (16 bits). The computer can store the 2 bytes in either order.
This order is called the **byte order** or **endianness**:

- **little-endian**: the low (small) byte comes first. Most PCs and the Raspberry Pi use this.
- **big-endian**: the high byte comes first.

`int.from_bytes` turns bytes into an int. You must say which order to use:

```python
print(int.from_bytes(b"\x34\x12", "little"))   # 4660  which is 0x1234
print(int.from_bytes(b"\x34\x12", "big"))      # 13330 which is 0x3412
```

**Signed** numbers can be negative. Use `signed=True` for them. Then a 16-bit value of 32768 or more counts
as negative. Its value is the number minus 65536. C++ stores a `short` (`std::int16_t`) in the same way:

```python
print(int.from_bytes(b"\xff\xff", "little", signed=True))   # -1
print(int.from_bytes(b"\xff\xff", "little"))                # 65535
```

### A first look at struct

The `struct` module is built in (`import struct`). It does the same job with short format codes. The next
module uses it a lot. The codes mean:

- `<` means little-endian.
- `H` means unsigned 16-bit.
- `h` means signed 16-bit.

```python
import struct
print(struct.unpack("<H", b"\x34\x12"))    # (4660,)
print(struct.unpack("<h", b"\xff\xff"))    # (-1,)
```

It always returns a **tuple** (a fixed list written with round brackets). It does this even for one value.
So take item `[0]`. The bytes you give it must be exactly the right length (2 for `H`).

### XOR and a simple checksum

`^` is **XOR** ("exclusive or"). It compares two numbers bit by bit. The result bit is 1 where the two bits
are **different**:

```python
print(bin(0b1100 ^ 0b1010))   # 0b110
print(hex(0x4f ^ 0x4b))       # 0x4      the bytes of b"OK"
```

A **checksum** is a small number that you calculate from data and send with it. The receiver calculates it
again. If the two numbers are different, the data was damaged on the way. Here is the simplest checksum:
start at 0, then XOR in every byte.

### Walking through a buffer

A **buffer** is a block of bytes that you have received. To read it one field at a time, keep a **position**
(an index). After you read a field, move the position forward by the size of that field. A `while` loop
does this:

```python
data = b"\x01\x00\x02\x00\x03\x00"     # three 2-byte little-endian numbers
pos = 0
values = []
while pos + 2 <= len(data):            # is a whole field still left?
    values.append(int.from_bytes(data[pos:pos + 2], "little"))
    pos += 2                           # move past the field we just read
print(values)                          # [1, 2, 3]
```

**New words**
- bit: a single 0 or 1. byte: 8 bits, a whole number from 0 to 255.
- binary / hex: ways to write numbers in base 2 (`0b101`) or base 16 (`0xff`).
- bytes: Python's type for raw data, written `b"..."`. Each item is an int from 0 to 255.
- encode / decode: encode turns str into bytes. decode turns bytes into str.
- endianness (byte order): which byte of a multi-byte number comes first. Little-endian puts the low byte first.
- signed: able to be negative.
- struct: a built-in module. It unpacks numbers from bytes with format codes like `<H`.
- tuple: a list that you cannot change, written with round brackets, like `(4660,)`.
- XOR (`^`): compares bit by bit. The result is 1 where the two bits are different.
- checksum: a small number calculated from data. It helps you find damage.
- buffer: a block of received bytes. position: the index where you are reading in it.

## Offline help

- Offline: `python3 -m pydoc bytes`, `python3 -m pydoc struct`
