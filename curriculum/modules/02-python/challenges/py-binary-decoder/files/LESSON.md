# Decode Binary Records: lesson

### 1. Bytes

Computers store everything as bytes. One byte is a whole number from
0 to 255. People often write bytes in hexadecimal ("hex", base 16).
In hex, 0xFF means 255 and 0x10 means 16.

Try to open samples.bin with `cat samples.bin`. You see strange
characters. This is because the file is not text. It is numbers.

### 2. Binary mode

Open this kind of file with "rb" (read binary). You get a bytes object,
not a string:

```
with open(path, "rb") as f:
    data = f.read()
len(data)      # how many bytes
data[0]        # first byte, as a number 0..255
```

### 3. Bigger numbers use several bytes

One byte can only hold numbers up to 255. So a frequency like 145800000
needs 4 bytes (32 bits). The order of those bytes is called endianness:

- **little-endian (LE)**: smallest part first. Most PCs and the Pi use it.
- **big-endian**: biggest part first.

Example with the two bytes 01 02:

```
little-endian reading: 0x0201 = 513
big-endian reading:    0x0102 = 258
```

The bytes are the same, but the number is different. So a file format
must say which order it uses.

### 4. Signed and unsigned

- "Unsigned" numbers are never negative. Example: uint32 holds 0 to about
  4.29 billion.
- "Signed" numbers can be negative. Example: int16 holds -32768 to 32767.

Power in dB is often negative. So it is stored as a signed number.

### 5. The struct module

The `struct` module reads and writes these layouts. You describe the
layout with a short format string:

```
<   little-endian (and no hidden padding bytes)
I   unsigned 32-bit int (4 bytes)
h   signed 16-bit int   (2 bytes)
H   unsigned 16-bit int (2 bytes)
B   unsigned 8-bit int  (1 byte)
```

Examples:

```
import struct
struct.unpack("<H", b"\x01\x02")      # (513,)  a tuple
struct.calcsize("<hB")                # 3 bytes per record
list(struct.iter_unpack("<hB", b"\xff\xff\x07\x02\x00\x01"))
# [(-1, 7), (2, 1)]   one tuple per 3-byte record
```

`unpack` reads exactly one record. `iter_unpack` reads many records,
one after another.

### 6. Refuse incomplete data

For iter_unpack, the data length must be an exact multiple of the record
size. Check this yourself first. Use % (the remainder operator):

```
10 % 3     # 1, so 10 bytes is NOT a whole number of 3-byte records
```

If there are bytes left over, raise ValueError. (You learned raise in the
previous challenge.) `./check` tries a 3-byte file. It expects ValueError.

decode_records must return a list of tuples. A tuple is a fixed list in
round brackets, like (1, 2). Return one tuple per record, in the same
order as the file.

The main block already writes the tuples to decoded.csv. Look at it with
`cat decoded.csv`.

Note: `./check` writes new, known values into samples.bin.

## New words
- **byte**: a number 0..255. It is the basic unit of computer storage.
- **hex (hexadecimal)**: base-16 writing of numbers, like 0xFF = 255.
- **binary file**: a file of raw bytes, not human-readable text.
- **endianness**: the order in which the bytes of a multi-byte number are stored.
- **little-endian (LE)**: least significant (smallest) byte first.
- **signed / unsigned**: signed numbers can be negative. Unsigned numbers cannot.
- **uint32, int16, uint8**: unsigned 32-bit, signed 16-bit, unsigned 8-bit int.
- **struct**: a Python module. It packs and unpacks binary layouts.
- **tuple**: a fixed list written with round brackets, like (1, 2).
- **record**: one fixed-size group of fields. It repeats through a file.
