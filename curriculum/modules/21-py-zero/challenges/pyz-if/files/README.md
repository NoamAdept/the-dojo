# Decisions: if, elif, else

**What you will learn:** how to make your code choose between different actions.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

Replace each `raise NotImplementedError` in `tasks.py`.

1. **is_even**: `is_even(n)` returns `True` if `n` is even. It returns `False` if `n` is odd. (Hint: use the remainder `n % 2`.)
2. **sign**: `sign(n)` returns `"negative"`, `"zero"` or `"positive"`.
3. **band**: `band(mhz)` gives the name of the radio band for a frequency in MHz:
   - below 30 is `"HF"`
   - from 30 up to 300 (but not 300 itself) is `"VHF"`
   - from 300 up to 3000 (but not 3000 itself) is `"UHF"`
   - 3000 or more is `"SHF"`
4. **can_listen**: `can_listen(has_antenna, has_power)` returns `True` only when both are `True`.
5. **largest**: `largest(a, b, c)` returns the biggest of the three numbers. Use `if`. Do not use the built-in `max`.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
