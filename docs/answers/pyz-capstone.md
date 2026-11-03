## Capstone: a Command-line Program

*pyz-capstone · easy*

**Goal.** Finish `report.py` so that `python3 report.py readings.txt` reads station readings, keeps the best SNR per station, and writes a sorted `report.txt`.

**You need to know.**

- `split(",", 1)`, `int(...)` and `raise ValueError(...)`.
- Dicts as "best so far" stores, `in` to test for a key, and `sorted(dict)` to get the keys in order.
- Chaining small functions into one `main`.
- `sys.argv` and the `if __name__ == "__main__":` block (README lesson).

**Walkthrough.**

1. Look at the input and the starter. `read_lines` and `write_lines` are already done.

   ```bash
   cat readings.txt
   vim report.py
   ```

2. Task 1: `parse_reading`.

   ```python
   def parse_reading(line):
       if "," not in line:
           raise ValueError(f"bad reading line: {line!r}")
       parts = line.split(",", 1)
       return [parts[0].strip(), int(parts[1])]
   ```

   Check for the comma first so a bad line stops with a clear `ValueError`; `int()` turns the SNR text into a number so it can be compared.

3. Task 2: `best_snr`.

   ```python
   def best_snr(lines):
       best = {}
       for line in lines:
           name, snr = parse_reading(line)
           if name not in best or snr > best[name]:
               best[name] = snr
       return best
   ```

   Store the value the first time a station appears, and replace it only when a bigger SNR comes along. `name not in best` is tested first so `best[name]` never raises `KeyError`.

4. Task 3: `report_lines`.

   ```python
   def report_lines(best):
       return [f"{name}: {best[name]}" for name in sorted(best)]
   ```

   `sorted(best)` gives the dict's keys in alphabetical order, and the f-string makes `"station: snr"`.

5. Task 4: `main` chains everything.

   ```python
   def main(path):
       write_lines("report.txt", report_lines(best_snr(read_lines(path))))
   ```

   Read from the inside out: read clean lines, find the best SNRs, format them, write them to `report.txt`.

6. Task 5: the main block, at the very bottom, not indented.

   ```python
   if __name__ == "__main__":
       main(sys.argv[1])
   ```

   This runs only when the file is started with `python3`, not when `./check` imports it. `sys.argv[1]` is the first word after the script name.

7. Run it from the shell.

   ```bash
   python3 report.py readings.txt
   cat report.txt
   ```

   Expected output:

   ```text
   beacon: 7
   harbour: 9
   tower: 15
   ```

8. Run the check.

   ```bash
   ./check
   ```

**Check.** `./check` prints `5/5 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Forgetting `int()` in `parse_reading`: then `"9" > "12"` compares as text and the wrong SNR wins.
- Calling `main(...)` at the bottom without the `__name__` guard: `./check` imports the file and it crashes on `sys.argv[1]`.
- Writing `sys.argv[0]` (that is the script name, `report.py`), or running `python3 report.py` with no file name, which gives `IndexError`.
