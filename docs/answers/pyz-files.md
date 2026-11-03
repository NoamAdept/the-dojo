## Reading and Writing Files

*pyz-files · easy*

**Goal.** Write five functions in `tasks.py` that read a file whole, count its lines, read clean lines, write lines, and combine read and write into `shout_file`.

**You need to know.**

- `with open(path) as f:` opens a file and closes it at the end of the block (README lesson).
- `f.read()` gives the whole text; `for line in f:` gives one line at a time, newline included.
- `open(path, "w")` creates or overwrites a file, and `f.write(...)` does not add a newline for you.
- `strip()`, `startswith()`, and list comprehensions from earlier challenges.

**Walkthrough.**

1. Look at the sample file, then open `tasks.py`.

   ```bash
   cat notes.txt
   vim tasks.py
   ```

   `notes.txt` has comment lines and a blank line, which is exactly what task 3 must skip.

2. Task 1: `read_all`.

   ```python
   def read_all(path):
       with open(path) as f:
           return f.read()
   ```

   `read()` returns the whole file as one string; returning inside `with` still closes the file.

3. Task 2: `count_lines`.

   ```python
   def count_lines(path):
       count = 0
       with open(path) as f:
           for line in f:
               count += 1
       return count
   ```

   Looping over a file object yields one line per pass, so counting passes counts lines. An empty file gives 0.

4. Task 3: `read_lines`.

   ```python
   def read_lines(path):
       lines = []
       with open(path) as f:
           for line in f:
               line = line.strip()
               if line and not line.startswith("#"):
                   lines.append(line)
       return lines
   ```

   Strip first so the newline and padding are gone; then an empty string is false, which skips blank lines, and `startswith("#")` skips comments.

5. Task 4: `write_lines`.

   ```python
   def write_lines(path, lines):
       with open(path, "w") as f:
           for line in lines:
               f.write(line + "\n")
   ```

   `"w"` opens for writing, and each line needs its own `"\n"` because `write` adds nothing.

6. Task 5: `shout_file` reuses tasks 3 and 4.

   ```python
   def shout_file(src, dst):
       write_lines(dst, [line.upper() for line in read_lines(src)])
   ```

   `read_lines` gives the clean lines, the comprehension upper-cases each one, and `write_lines` saves them.

7. Try it on the sample, then check.

   ```bash
   python3 -c "import tasks; print(tasks.read_lines('notes.txt'))"
   ./check
   ```

   The first command should print `['tower is loud tonight', 'beacon is faint']`.

**Check.** `./check` prints `5/5 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Forgetting `"\n"` in `write_lines`, so all lines end up glued on one line.
- Testing `startswith("#")` before stripping, so a line like `"  # note"` slips through (or blank lines stay in).
- Opening with `"w"` when they meant to read: it empties the file. Warn them not to try that on `notes.txt`.
