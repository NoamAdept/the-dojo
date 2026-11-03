## Automate a Signal Investigation

*py-auto-investigator · medium*

**Goal.** Complete `investigate(input_path, output_path)` in `investigate.py` so it reads a CSV of observations, keeps only `LOCKED` rows, groups them by station, and writes JSON with the count and one-decimal average SNR for every station seen at least three times.

**You need to know.**

- `csv.DictReader` gives each row as a dict of strings (README lessons 1 and 2).
- Filter, then group into a dict of lists (README lesson 3, and pyz-text-dicts).
- `float(...)`, `sum`, `len` and `round(x, 1)`.
- `json.dump(..., sort_keys=True, indent=2)` (README lesson 4).

**Walkthrough.**

1. Look at the data and try the starter.

   ```bash
   cat observations.csv
   ./run
   ```

   With the stub, `./run` fails with `FileNotFoundError: ... 'report.json'`, because `investigate` writes nothing yet.

2. Replace the `# TODO` and `pass` with three parts. First, read, filter and group:

   ```python
       groups = {}
       with open(input_path, newline="") as f:
           for row in csv.DictReader(f):
               if row["status"] != "LOCKED":
                   continue
               station = row["station"]
               if station not in groups:
                   groups[station] = []
               groups[station].append(float(row["snr"]))
   ```

   Each row is a dict keyed by the header names. Non-LOCKED rows are skipped before anything is stored, and `float()` turns the SNR text into a number we can average.

3. Second, keep only stations with three or more readings and work out the numbers:

   ```python
       result = {}
       for station, values in groups.items():
           if len(values) >= 3:
               result[station] = {
                   "count": len(values),
                   "average_snr": round(sum(values) / len(values), 1),
               }
   ```

   `len` is the count of LOCKED rows, and `round(..., 1)` gives one decimal place.

4. Third, write the JSON:

   ```python
       with open(output_path, "w") as f:
           json.dump(result, f, sort_keys=True, indent=2)
   ```

   `sort_keys=True` orders the stations (and the inner keys) alphabetically, so the same input always gives the same file.

5. Run it on the sample data.

   ```bash
   ./run
   ```

   You see `ALPHA` with `count` 3 and `average_snr` 15.0, and `CHARLIE` with `count` 3 and `average_snr` 9.0. `BRAVO` is missing because its only row was `SEARCHING`.

6. Run the check.

   ```bash
   ./check
   ```

   The check uses a different CSV (other station names), so nothing may be typed in by hand.

**Check.** `./check` prints `CHECK_OK`. Press Done in the dojo to get the flag.

**Common mistakes.**

- Counting rows before filtering, so a station with two LOCKED and one SEARCHING row wrongly reaches three. The check data has exactly this trap (station ANN).
- Forgetting `float()`: `sum` on strings raises `TypeError`.
- Hard-coding `ALPHA` and `CHARLIE`, or writing to `"report.json"` instead of `output_path`; the check uses its own paths and data.
