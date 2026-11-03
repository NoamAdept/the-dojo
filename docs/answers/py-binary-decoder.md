## Decode Binary Sensor Records

*py-binary-decoder · medium*

**Goal.** Complete `decode_records(path)` in `decode.py` so it reads `samples.bin` as 7-byte records (uint32 frequency, int16 power, uint8 status, all little-endian), returns a list of tuples, and raises `ValueError` on leftover bytes. The provided main block then writes `decoded.csv`.

**You need to know.**

- Opening a file in binary mode with `"rb"` (README lesson 2).
- Little-endian and signed versus unsigned (README lessons 3 and 4, and pyz-bytes-hex).
- `struct` format letters `<`, `I`, `h`, `B`, plus `calcsize` and `iter_unpack` (README lesson 5).
- `%` to spot an incomplete last record (README lesson 6).

**Walkthrough.**

1. Look at the starter and run it once.

   ```bash
   vim decode.py
   python3 decode.py samples.bin
   cat decoded.csv
   ```

   With the stub, `decoded.csv` holds only the header line, because `decode_records` returns `[]`.

2. Work out the format string. The layout is uint32 + int16 + uint8, little-endian:

   ```python
   import struct
   struct.calcsize("<IhB")    # 7
   ```

   `<` also turns off padding, so the size is exactly 4 + 2 + 1 = 7 bytes, matching the README.

3. Replace the `# TODO` and `return []` in `decode_records` with:

   ```python
   def decode_records(path):
       with open(path, "rb") as f:
           data = f.read()
       size = struct.calcsize("<IhB")
       if len(data) % size != 0:
           raise ValueError(f"{len(data) % size} trailing bytes do not form a record")
       return list(struct.iter_unpack("<IhB", data))
   ```

   - `"rb"` gives a `bytes` object, not text.
   - A non-zero remainder means the last record is cut short, so we refuse the file instead of guessing.
   - `iter_unpack` reads one tuple per 7 bytes in file order; `list(...)` turns it into the list the check compares.

4. Run the program again.

   ```bash
   python3 decode.py samples.bin
   cat decoded.csv
   ```

   You now see the header and one row per record, for example `145800000,-42,1`. The negative powers prove `h` (signed) is right.

5. Run the check.

   ```bash
   ./check
   ```

   It rewrites `samples.bin` with three known records, compares your tuples, feeds a 3-byte file expecting `ValueError`, and runs the script.

**Check.** `./check` prints `CHECK_OK`. Press Done in the dojo to get the flag.

**Common mistakes.**

- Forgetting `<`: native mode adds padding, `calcsize("IhB")` becomes 8 on most machines and every value is wrong.
- Using `H` instead of `h`: the power reads as large positive numbers (like 65494) instead of -42.
- Opening with `"r"` instead of `"rb"`: Python tries to decode the bytes as text and fails or mangles them.
