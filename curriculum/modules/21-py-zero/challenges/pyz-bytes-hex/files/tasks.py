"""Python from Zero 10: bytes, hex and binary."""
import struct


def to_hex(n):
    """Task 1: 255 -> "0xff"."""
    raise NotImplementedError


def from_hex(text):
    """Task 1: "ff" -> 255, "0x1a" -> 26."""
    raise NotImplementedError


def to_binary(n):
    """Task 1: 5 -> "101" (no 0b)."""
    raise NotImplementedError


def text_to_bytes(text):
    """Task 2: "Hi" -> b"Hi"."""
    raise NotImplementedError


def bytes_to_text(data):
    """Task 2: b"Hi" -> "Hi"."""
    raise NotImplementedError


def parse_hex(text):
    """Task 3: "48 69 21" -> b"Hi!"."""
    raise NotImplementedError


def show_hex(data):
    """Task 3: b"Hi!" -> "486921"."""
    raise NotImplementedError


def byte_values(data):
    """Task 4: b"Hi!" -> [72, 105, 33]."""
    raise NotImplementedError


def last_byte(data):
    """Task 4: the last byte as an int."""
    raise NotImplementedError


def read_u16(data, pos):
    """Task 5: unsigned little-endian 16-bit number at data[pos], data[pos + 1]."""
    raise NotImplementedError


def read_i16(data, pos):
    """Task 5: signed little-endian 16-bit number at data[pos], data[pos + 1]."""
    raise NotImplementedError


def read_u16_struct(data, pos):
    """Task 6: like read_u16, using struct.unpack("<H", ...)."""
    raise NotImplementedError


def xor_checksum(data):
    """Task 7: XOR of every byte, 0 for empty data."""
    raise NotImplementedError


def split_chunks(data):
    """Task 8: b"\\x02hi\\x03abc" -> [b"hi", b"abc"]; ValueError if a chunk is cut short."""
    raise NotImplementedError
