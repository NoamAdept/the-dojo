# Sensor Bones

`py-binary-decoder` · Blue Belt

**Goal:** Complete `decode_records(path)` in `decode.py` so it reads `samples.bin` as 7-byte records (uint32 frequency, int16 power, uint8 status, all little-endian), returns a list of tuples, and raises `ValueError` on leftover bytes. The provided main block then writes `decoded.csv`.

**File `decode.py`**

```python
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
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
