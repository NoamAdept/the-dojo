# Data Types and Dynamic Typing



## Module 2: Data Types and Dynamic Typing

Welcome to Module 2. In this part, you learn how Python handles data. Python is **dynamically typed**, unlike C++. This means a value has a type, but a variable name does not. This changes how you write code and how you think about it.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

Write the functions and the class in `tasks.py`.

1. **String slicing**: `extract_program(s)` takes `"PythonProgramming"`. It returns the `"Program"` part. Use a slice.
2. **F-string conversion**: `format_item(item, price)` returns `"Item: Apples | Cost: $2.50"` for `("Apples", 2.5)`.
3. **Safe division**: `safe_div(a, b)` follows these rules:
   - It returns `a / b` when both values are int or float (but not bool).
   - It returns `None` when a value is not a number.
   - It returns `None` for division by zero.
4. **Type hinting**: add type hints to `power(base, exp)`. Both arguments are `float`. The result is `float`.
5. **Palindrome checker**: `is_palindrome(text: str) -> bool` ignores upper/lower case and spaces. So `"Race Car"` is a palindrome (it reads the same in both directions).
6. **Data cleaner**: `clean_numbers(items)` returns only the valid numbers, as floats. Use `try`/`except` to skip strings that are not numbers. For example, `["10", "2.5", "invalid", 5, 20.0]` gives `[10.0, 2.5, 5.0, 20.0]`.
7. **Custom number type**: `HexNumber("0xA")` must support `int(h) == 10` and `str(h) == "0xa"`. The string uses lowercase and starts with `0x`.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
