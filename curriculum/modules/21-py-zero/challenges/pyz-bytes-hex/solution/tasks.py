"""Python from Zero 10: bytes, hex and binary."""
import struct


def to_hex(n):
    return hex(n)


def from_hex(text):
    return int(text, 16)


def to_binary(n):
    return bin(n)[2:]


def text_to_bytes(text):
    return text.encode()


def bytes_to_text(data):
    return data.decode()


def parse_hex(text):
    return bytes.fromhex(text)


def show_hex(data):
    return data.hex()


def byte_values(data):
    return list(data)


def last_byte(data):
    return data[-1]


def read_u16(data, pos):
    return int.from_bytes(data[pos:pos + 2], "little")


def read_i16(data, pos):
    return int.from_bytes(data[pos:pos + 2], "little", signed=True)


def read_u16_struct(data, pos):
    return struct.unpack("<H", data[pos:pos + 2])[0]


def xor_checksum(data):
    check = 0
    for b in data:
        check ^= b
    return check


def split_chunks(data):
    chunks = []
    pos = 0
    while pos < len(data):
        length = data[pos]
        start = pos + 1
        if start + length > len(data):
            raise ValueError("chunk runs past the end")
        chunks.append(data[start:start + length])
        pos = start + length
    return chunks
