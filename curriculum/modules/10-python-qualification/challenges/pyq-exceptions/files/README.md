# Error and Exception Handling



## Module 9: Error and Exception Handling

Python uses exceptions as the main way to report and handle errors. C uses error codes instead. Modern C++ uses exceptions too, so Python is similar to it. Python programmers often say: "It is easier to ask for forgiveness than permission" (EAFP). This means: try the action first, and handle the error if it fails.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

1. **Input validator**: `read_int(inputs)` takes an iterator of strings (it replaces `input()`). For each string that is not an integer, it prints `"Invalid"`. It returns the first valid int.
2. **List bounds**: `safe_get(lst, i)` returns `lst[i]`. If it catches `IndexError`, it returns `None`.
3. **Custom error**: write `InvalidAgeError(ValueError)` and `set_age(age)`. `set_age` raises the error when the age is outside 0–150. Otherwise it returns the age.
4. **Clean up**: `use_resource(log, fail)` does 3 things (use `try`/`finally`):
   - It appends `"open"`.
   - It raises `RuntimeError` if `fail` is true.
   - It always appends `"closed"`.
5. **Safe calculator**: `safe_divide(a, b)` returns `a / b`.
   - On `ZeroDivisionError`, it returns `float("inf")`.
   - On `TypeError`, it prints `"Inputs must be numbers"` and returns `None`.
6. **Retry decorator**: `retry(attempts=3)` runs the function again when it raises an exception. Before each new attempt, it prints `"Retrying..."`. When no attempts are left, it raises the last exception again.
7. **Transaction processor**: write `Account(name, balance)`.
   - `transfer(amount, target, accounts)` raises `InsufficientFunds`, or `InvalidAccount` when the target name is not in the `accounts` dict.
   - `process_batch(batch, accounts)` runs a list of `(source, target, amount)` triples. It logs each failure as a string and keeps going. It returns `(succeeded_count, error_messages)`.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
