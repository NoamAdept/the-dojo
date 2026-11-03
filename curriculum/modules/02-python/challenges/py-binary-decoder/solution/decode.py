#!/usr/bin/env python3
import csv
import struct
import sys

def decode_records(path):
    with open(path, "rb") as f:
        data = f.read()
    size = struct.calcsize("<IhB")
    if len(data) % size != 0:
        raise ValueError(f"{len(data) % size} trailing bytes do not form a record")
    return list(struct.iter_unpack("<IhB", data))

if __name__ == "__main__":
    rows = decode_records(sys.argv[1])
    with open("decoded.csv", "w", newline="") as f:
        out = csv.writer(f)
        out.writerow(["frequency_hz", "power_db", "status"])
        out.writerows(rows)
