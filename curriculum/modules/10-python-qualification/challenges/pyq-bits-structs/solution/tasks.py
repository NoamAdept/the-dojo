"""Python Qualification 11: bit manipulation and structs."""
import struct


def bit_state(value, n):
    return "ON" if (value >> n) & 1 else "OFF"


def clear_low_nibble(value):
    return value & ~0xF


def pack_reading(b, f, s):
    return struct.pack("<Bfh", b, f, s)


def endian_bytes(value):
    return value.to_bytes(4, "big").hex(), value.to_bytes(4, "little").hex()


def count_set_bits(n):
    return bin(n).count("1")


def parse_packet(data):
    if len(data) != 7:
        raise ValueError(f"expected 7 bytes, got {len(data)}")
    header, pid, payload = struct.unpack(">HBI", data)
    if header != 0xAA55:
        raise ValueError(f"bad header {header:#06x}")
    return pid, payload


def get_bmp_dimensions(path):
    with open(path, "rb") as fh:
        head = fh.read(26)
    if head[:2] != b"BM":
        raise ValueError("not a BMP file")
    return struct.unpack_from("<ii", head, 18)
