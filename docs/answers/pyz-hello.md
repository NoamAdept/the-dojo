## Hello, Python

*pyz-hello · easy*

**Goal.** Create three small `.py` files (`hello.py`, `arith.py`, `label.py`) that print exact text, and fix the two mistakes in `broken.py` so it runs.

**You need to know.**

- How to run `python3` interactively and how to run a file with `python3 NAME.py` (README, "The interactive prompt" and "A .py file").
- `print(...)` with one or several comma-separated values (README, "A .py file").
- Python division: `/` gives a float, `//` drops the remainder, `%` is the remainder, `**` is power.
- How to read an error: last line first, then the line number (README, "Errors").

**Walkthrough.**

1. Check Python is installed and play at the prompt for a minute.

   ```bash
   python3 --version
   python3        # try 7 / 2 and 7 // 2, then exit() or Ctrl-D
   ```

   This shows the learner that the REPL answers each line at once, which helps for task 2.

2. Task 1: make `hello.py` with `vim hello.py`, press `i`, type one line, then press `Esc` and type `:wq` Enter.

   ```python
   print("Hello, Pi!")
   ```

   The text is in quotes so Python treats it as a string, and `print` adds the newline by itself. Run `python3 hello.py` to see it.

3. Task 2: make `arith.py` with four prints, one per sum.

   ```python
   print(7 / 2)
   print(7 // 2)
   print(7 % 2)
   print(2 ** 10)
   ```

   Each `print` is its own line of output, and Python works out each sum, giving `3.5`, `3`, `1` and `1024`.

4. Task 3: make `label.py` with a single `print` of three values.

   ```python
   print("Rate", 2048000, "Hz")
   ```

   `print` puts exactly one space between the values, so no spaces are needed inside the quotes.

5. Task 4: run `broken.py` and read the error.

   ```bash
   python3 broken.py
   ```

   The first error is `SyntaxError: '(' was never closed` on line 2. Add the missing `)`. Run it again and the next error is `NameError: name 'Done' is not defined`, because `Done` without quotes looks like a variable name. The fixed file:

   ```python
   print("Signal found")
   print("Done")
   ```

6. Run the checker.

   ```bash
   ./check
   ```

**Check.** `./check` prints `4/4 tasks pass` and then `CHECK_OK`. Press Done in the dojo.

**Common mistakes.**

- Typing the answers into `arith.py` (`print(3.5)`) instead of the sums. It passes the check, but misses the point; nudge them back to `print(7 / 2)`.
- Adding extra spaces in task 3 (`"Rate "`), which gives two spaces in the output.
- Wrong capitals or punctuation in `Hello, Pi!`; the check wants it exactly.
