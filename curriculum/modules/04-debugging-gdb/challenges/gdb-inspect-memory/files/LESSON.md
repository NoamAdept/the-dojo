# Inspect Memory: lesson

print shows a value in the same way your C++ program sees it. But sometimes you want to see the raw bytes at an address. GDB's x command ("examine") does that.

```
x/NFU ADDRESS
   N   how many units to show, e.g. 8
   F   format: x = hex, d = decimal, c = character
   U   unit size: b = byte, h = 2 bytes, w = 4 bytes

x/8bx buf    8 units, each a byte, shown in hex
```

ADDRESS can be a pointer variable. Then x follows the pointer to the memory it points at.

Remember from C++ Under the Hood: a pointer holds an address. In this target, packet is a pointer to the first byte of an array of 8 bytes. The array type is std::uint8_t, the unsigned type that is 1 byte long.

Here is an example with a different program. It is paused in `look(const std::uint8_t *buf)`, and buf points at 10 bytes:

```
(gdb) x/10bx buf
0x7fffffffb38e:   0x48  0x69  0x21  0x0a  0x00  0x07  0xff  0x10
0x7fffffffb396:   0x20  0x30
```

How to read it:

- The part before the colon is the address of the first byte on that line. Ignore it.
- After the colon come the bytes, in memory order.
- GDB starts a new line after 8 bytes. The second line just continues the first.

Your addresses will be different every time. The bytes will be the same.

You can also see the same bytes in decimal:

```
(gdb) x/4bd buf
0x7fffffffb38e:   72   105   33   10
```

print buf is less useful here. It shows the pointer, and it tries to read the bytes as text. It stops at the first 0x00 byte.

Tidying hex. Each byte is 2 hex digits. To write bytes in the usual plain form:

1. Remove the 0x.
2. Keep both digits. Keep a leading zero too: 0x0a becomes 0a, and 0x00 becomes 00.
3. Use lowercase letters.

The example above becomes:

```
48 69 21 0a 00 07 ff 10 20 30
```

## New words
- **x (examine)**: GDB command that shows raw memory at an address.
- **unit**: the size of each item that x shows (byte, halfword, word).
- **memory order**: the order of the bytes in memory, lowest address first.
- **address**: where in memory something is, shown in hex.
- **leading zero**: the 0 in 0a that keeps every byte 2 digits long.
- **pointer**: a variable that holds an address.

## Offline help

- Inside GDB: help x
