## Decisions: if, elif, else

*pyz-if · easy*

**Goal.** Write five small functions in `tasks.py` that make decisions with comparisons, `and`, and `if` / `elif` / `else`.

**You need to know.**

- Comparisons (`<`, `==`, `>=`) already give `True` or `False`.
- `if` / `elif` / `else`: only the first branch whose test is true runs (README lesson).
- `and` is true only when both sides are true.
- Function basics and indentation from pyz-functions.

**Walkthrough.**

1. Open `tasks.py` and, for each function, replace `raise NotImplementedError` with the body below (indented 4 spaces, nested blocks 8).

2. Task 1: `is_even`.

   ```python
   def is_even(n):
       return n % 2 == 0
   ```

   The remainder after dividing by 2 is 0 for even numbers, and the comparison itself is the `True`/`False` answer, so no `if` is needed.

3. Task 2: `sign`.

   ```python
   def sign(n):
       if n < 0:
           return "negative"
       elif n == 0:
           return "zero"
       else:
           return "positive"
   ```

   Three cases, three branches; `else` catches everything left over, so floats like `0.1` work too.

4. Task 3: `band`. Test the smallest range first.

   ```python
   def band(mhz):
       if mhz < 30:
           return "HF"
       elif mhz < 300:
           return "VHF"
       elif mhz < 3000:
           return "UHF"
       else:
           return "SHF"
   ```

   An `elif` only runs when every earlier test failed, so when we reach `mhz < 300` we already know `mhz >= 30`. Boundaries: 30 is VHF, 300 is UHF, 3000 is SHF.

5. Task 4: `can_listen`.

   ```python
   def can_listen(has_antenna, has_power):
       return has_antenna and has_power
   ```

   `and` gives `True` only when both values are `True`.

6. Task 5: `largest`, without `max`.

   ```python
   def largest(a, b, c):
       if a >= b and a >= c:
           return a
       elif b >= c:
           return b
       else:
           return c
   ```

   If `a` beats both others it wins; otherwise the answer is the bigger of `b` and `c`. Using `>=` handles ties like `(5, 5, 1)`.

7. Run the check.

   ```bash
   ./check
   ```

**Check.** `./check` prints `5/5 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Wrong boundaries in `band`, for example `mhz <= 30` for HF. The check tests exactly 30, 300 and 3000.
- Using `max(` anywhere in the file, even in a comment: the check searches the source for it and fails task 5.
- Using `>` instead of `>=` in `largest`, which breaks on ties.
