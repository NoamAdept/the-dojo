## Functions: def and return

*pyz-functions · easy*

**Goal.** Replace each `raise NotImplementedError` in `tasks.py` with a one-line body that returns the right value, and change `average` from `print` to `return`.

**You need to know.**

- `def name(params):` plus an indented body (README, the `add` example).
- Indentation decides which lines belong to the function, 4 spaces per level.
- `return` gives a value back; `print` only shows it (README, "return is not print").
- A function can call another function you wrote.

**Walkthrough.**

1. Open `tasks.py`. For each function, delete the `raise NotImplementedError` line and write the body in its place, indented 4 spaces. The docstrings can stay.

2. Task 1: `double`.

   ```python
   def double(n):
       return n * 2
   ```

   `return` hands `n * 2` back to the caller and ends the function.

3. Task 2: `greet`, with an f-string.

   ```python
   def greet(name):
       return f"Hello, {name}!"
   ```

   The f-string drops the argument into the text, so `greet("Ada")` gives `"Hello, Ada!"`.

4. Task 3 and task 4: `area` and `to_khz`.

   ```python
   def area(width, height):
       return width * height

   def to_khz(hz):
       return hz / 1000
   ```

   `/` always gives a float, so `to_khz(1500)` is `1.5`, which is what the check expects.

5. Task 5: fix `average`.

   ```python
   def average(a, b):
       return (a + b) / 2
   ```

   With `print` the caller got `None`; `return` gives the number back so it can be stored or tested.

6. Task 6: `quadruple` calls `double` twice.

   ```python
   def quadruple(n):
       return double(double(n))
   ```

   The inner call doubles `n`, the outer call doubles that. The check counts the calls, so `n * 4` alone fails.

7. Test at the prompt, then check.

   ```bash
   python3 -c "import tasks; print(tasks.double(4), tasks.greet('Pi'), tasks.average(2, 5))"
   ./check
   ```

**Check.** `./check` prints `6/6 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Keeping `print` in `average`: the check says it "gave back None".
- Mixing tabs and spaces, or forgetting to indent, gives `IndentationError` and the whole file fails to load.
- Writing `return n * 4` in `quadruple`: the value is right but the check wants two calls to `double`.
- Editing `tasks.py` while a `>>>` prompt is open: the old version stays loaded until they restart `python3`.
