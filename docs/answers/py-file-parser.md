## Parse a Receiver Configuration

*py-file-parser · easy*

**Goal.** Complete `parse_config(path)` in `parse_config.py` so it turns `name = value` lines into a dict of strings, skips blanks and `#` comments, and raises `ValueError` on a line with no `=`. Running the script writes `parsed.txt`.

**You need to know.**

- Reading a file line by line with `with open(path) as f:` and `strip()` (README lesson 2, and pyz-files).
- `continue` to skip a line (README lesson 3).
- `split("=", 1)` to split at the first `=` only (README lesson 4).
- `raise ValueError(...)` on bad input (README lesson 5).

**Walkthrough.**

1. Look at the input and the docstring.

   ```bash
   cat receiver.conf
   vim parse_config.py
   ```

   Note the tricky lines: `mode= FM` has odd spacing, there is a blank line, and `label = roof=antenna` has `=` in its value.

2. Replace the `# TODO` and `return {}` with this body.

   ```python
   def parse_config(path):
       """Return a dict from name=value lines; ignore blanks and # comments."""
       result = {}
       with open(path) as f:
           for line in f:
               line = line.strip()
               if line == "" or line.startswith("#"):
                   continue
               if "=" not in line:
                   raise ValueError("line without '=': " + line)
               name, value = line.split("=", 1)
               result[name.strip()] = value.strip()
       return result
   ```

   - `strip()` removes the newline and edge spaces, so blank lines become `""`.
   - `continue` skips blanks and comments without touching the dict.
   - The `"=" not in line` test comes after the skip, so only real setting lines can raise.
   - `split("=", 1)` keeps `roof=antenna` in one piece, and stripping both parts turns `" FM"` into `"FM"`.
   - Values stay strings (`"18"`, not `18`), which is what the check compares against.

3. Leave the main block alone. Run the program.

   ```bash
   python3 parse_config.py receiver.conf
   cat parsed.txt
   ```

   `parsed.txt` holds four sorted lines: `frequency=145800000`, `gain=18`, `label=roof=antenna`, `mode=FM`.

4. Run the check.

   ```bash
   ./check
   ```

   It also feeds a temporary file containing `broken line` and expects your `ValueError`.

**Check.** `./check` prints `CHECK_OK`. Press Done in the dojo to get the flag.

**Common mistakes.**

- `line.split("=")` without the `1`: `label = roof=antenna` gives three pieces and the unpacking fails.
- Converting values with `int()`: the check expects every value as a string.
- Checking for `=` before skipping comments, so a comment like `# classroom receiver` raises `ValueError`.
