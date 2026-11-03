## Variables, Types and f-strings

*pyz-values · easy*

**Goal.** Replace every `None` in `tasks.py` with a value of the right type, a conversion, or an f-string.

**You need to know.**

- `name = value` makes a variable; the type belongs to the value (README, "Variables").
- The four basic types `int`, `float`, `str`, `bool`, and `None` (README, "The basic types").
- `int(...)`, `float(...)`, `str(...)` convert between types (README, "Converting").
- f-strings and the `:.2f` format spec (README, "f-strings").

**Walkthrough.**

1. Open the file and look at it first.

   ```bash
   vim tasks.py
   ```

   Every value to fill in is `None`. Keep the variable names exactly as they are, because `./check` imports the file and reads them by name.

2. Tasks 1 to 4: the four basic types.

   ```python
   station = "Pi Radio"
   channels = 16
   gain_db = 20.5
   is_on = True
   ```

   Quotes make a `str`, a whole number makes an `int`, a decimal point makes a `float`, and `True` (capital T, no quotes) is a `bool`.

3. Task 5: convert the text to a number.

   ```python
   as_int = int(text_number)
   ```

   `int(...)` turns the string `"433"` into the integer `433`. The check reads the source, so typing `433` directly is rejected.

4. Task 6: build the label with an f-string.

   ```python
   label = f"{station} has {channels} channels"
   ```

   The `f` before the quote tells Python to replace each `{name}` with the variable's value.

5. Task 7: format the float to two decimals.

   ```python
   pi_text = f"{pi:.2f}"
   ```

   After the colon, `.2f` means "fixed point, 2 digits after the dot", so `3.14159` becomes the string `"3.14"`.

6. Try it at the prompt, then run the check.

   ```bash
   python3 -c "import tasks; print(tasks.label, tasks.pi_text)"
   ./check
   ```

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- `channels = "16"` or `gain_db = "20.5"`: in quotes these are strings, and the check reports the wrong type.
- `is_on = true` (lower case) gives a `NameError` when the file loads, so every task fails at once.
- Forgetting the `f` in front of the quote, which leaves the literal text `{station}` in the string.
