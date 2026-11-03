"""Writes pixel.bmp (a 3x2 24-bit image). Run: python3 make_bmp.py"""
import struct

width, height = 3, 2
row = (b"\x00\x00\xff" * width).ljust(12, b"\x00")  # rows pad to 4 bytes
pixels = row * height
header = struct.pack("<2sIHHI", b"BM", 54 + len(pixels), 0, 0, 54)
info = struct.pack("<IiiHHIIiiII", 40, width, height, 1, 24, 0, len(pixels), 2835, 2835, 0, 0)
with open("pixel.bmp", "wb") as fh:
    fh.write(header + info + pixels)
