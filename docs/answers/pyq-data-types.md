## Data Types and Dynamic Typing

*pyq-data-types · easy*

**Goal.** Fill in the six functions and the `HexNumber` class in `tasks.py`, and add type hints to `power`, until `./check` prints `CHECK_OK`.

**You need to know.**

- Slicing `s[start:stop]` and `s[::-1]` (README section 4).
- f-string format specs like `{x:.2f}` (README section 5).
- `isinstance` and the fact that `bool` is a subclass of `int` (README section 9).
- Type hints and `try`/`except` (README sections 7 and 10).
- `int(text, 16)`, `hex()` and the `__int__` / `__str__` dunders.

**Walkthrough.**

1. Run `./check` once to see all seven tasks listed as "not implemented yet".

   ```bash
   ./check
   ```

2. Task 1, slicing. "Python" is 6 letters and "Program" is 7, so the slice is 6 to 13 (stop is exclusive).

   ```python
   def extract_program(s):
       return s[6:13]
   ```

3. Task 2, f-string. `:.2f` always prints two decimals, so `35` becomes `35.00`. The `$` is a literal character.

   ```python
   def format_item(item, price):
       return f"Item: {item} | Cost: ${price:.2f}"
   ```

4. Task 3, safe division. Reject anything that is not an int or float, and reject `bool` explicitly because `isinstance(True, int)` is True. Catch only `ZeroDivisionError`.

   ```python
   def safe_div(a, b):
       ok = all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in (a, b))
       if not ok:
           return None
       try:
           return a / b
       except ZeroDivisionError:
           return None
   ```

5. Task 4, type hints. The check reads them with `typing.get_type_hints`, so all three must be `float`.

   ```python
   def power(base: float, exp: float) -> float:
       return base ** exp
   ```

6. Task 5, palindrome. Remove spaces and lowercase first, then compare with the reversed string.

   ```python
   def is_palindrome(text: str) -> bool:
       s = text.replace(" ", "").lower()
       return s == s[::-1]
   ```

7. Task 6, data cleaner. `float()` raises `ValueError` for `"invalid"` and `TypeError` for `None` (the check passes a `None`), so catch both.

   ```python
   def clean_numbers(items):
       out = []
       for item in items:
           try:
               out.append(float(item))
           except (TypeError, ValueError):
               continue
       return out
   ```

8. Task 7, `HexNumber`. `int(text, 16)` accepts the `0x` / `0X` prefix, and `hex()` always returns a lowercase `0x...` string.

   ```python
   class HexNumber:
       def __init__(self, text: str) -> None:
           self.value = int(text, 16)

       def __int__(self) -> int:
           return self.value

       def __str__(self) -> str:
           return hex(self.value)
   ```

**Check.** `./check` prints `7/7 tasks pass` and then `CHECK_OK`. The learner then presses Done in the dojo, which awards the flag.

**Common mistakes.**

- Slicing `s[6:12]` or `s[7:14]`: off by one because the stop index is exclusive.
- Forgetting that `True` is an int, so `safe_div(True, 1)` returns `1.0` instead of `None`.
- Catching only `ValueError` in `clean_numbers`; the `None` in the check's list raises `TypeError`.
