# Capstone: a Command-line Program

**What you will learn:** how to turn a few functions into a complete program. You run the program with a file name. The challenges in the next module have the same shape.

Only 3 things here are new. You have already done everything else.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

Fill in `report.py` (tasks 1 to 4). Then add the main block (task 5).

1. **parse_reading**: `parse_reading(line)` turns `"tower,12"` into `["tower", 12]`. The SNR must be an int. If the line has no comma, `raise ValueError`.
2. **best_snr**: `best_snr(lines)` takes a list of reading lines (strings). It returns a dict that maps each station to its **highest** SNR. Use `parse_reading` for each line.
3. **report_lines**: `report_lines(best)` turns that dict into a list of strings in the form `"station: snr"`. Sort the list by station name. For example, `{"tower": 15, "beacon": 4}` gives `["beacon: 4", "tower: 15"]`.
4. **main**: `main(path)` does 3 things:
   - It reads the file with `read_lines`.
   - It calculates the best SNRs.
   - It writes the report lines to `report.txt` with `write_lines`.
5. **Run it from the shell**: at the bottom of the file, add the `if __name__ == "__main__":` block. It calls `main(sys.argv[1])`. Then run `python3 report.py readings.txt` and `cat report.txt`. You should see:

   ```text
   beacon: 7
   harbour: 9
   tower: 15
   ```

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
