## Error and Exception Handling

*pyq-exceptions · medium*

**Goal.** Implement the functions, the `retry` decorator and the `Account` / `process_batch` transaction code in `tasks.py`, catching the right exceptions in the right places.

**You need to know.**

- `try` / `except` / `else` / `finally`, and catching the narrowest exception.
- Custom exception classes that subclass `ValueError` or `Exception`.
- A decorator that takes arguments is three functions deep.
- `raise` with no argument re-raises the current exception.

**Walkthrough.**

1. Run `./check` to see the failures.

   ```bash
   ./check
   ```

2. Task 1, input validator. Loop over the iterator; `return` leaves on the first good value, and `ValueError` (from `int("x")` or `int("4.5")`) prints `Invalid`.

   ```python
   def read_int(inputs):
       for text in inputs:
           try:
               return int(text)
           except ValueError:
               print("Invalid")
   ```

3. Task 2, list bounds.

   ```python
   def safe_get(lst, i):
       try:
           return lst[i]
       except IndexError:
           return None
   ```

4. Task 3, custom error. The class is already in the starter; raise it when the age is outside 0 to 150.

   ```python
   def set_age(age):
       if not 0 <= age <= 150:
           raise InvalidAgeError(f"age out of range: {age}")
       return age
   ```

5. Task 4, clean up. `finally` runs whether or not the `RuntimeError` is raised, and the error still propagates to the caller.

   ```python
   def use_resource(log, fail):
       log.append("open")
       try:
           if fail:
               raise RuntimeError("resource failure")
       finally:
           log.append("closed")
   ```

6. Task 5, safe calculator. Two `except` branches, one per error type.

   ```python
   def safe_divide(a, b):
       try:
           return a / b
       except ZeroDivisionError:
           return float("inf")
       except TypeError:
           print("Inputs must be numbers")
           return None
   ```

7. Task 6, retry decorator. `retry(attempts)` returns `decorator`, which returns `wrapper`. On the last attempt the bare `raise` re-raises; otherwise it prints and loops again.

   ```python
   def retry(attempts=3):
       def decorator(func):
           @functools.wraps(func)
           def wrapper(*args, **kwargs):
               for attempt in range(1, attempts + 1):
                   try:
                       return func(*args, **kwargs)
                   except Exception:
                       if attempt == attempts:
                           raise
                       print("Retrying...")
           return wrapper
       return decorator
   ```

8. Task 7, transactions. In `Account.transfer`, check the target first, then the balance, then move the money.

   ```python
   def transfer(self, amount, target, accounts):
       if target not in accounts:
           raise InvalidAccount(target)
       if amount > self.balance:
           raise InsufficientFunds(f"{self.name} has {self.balance}, needs {amount}")
       self.balance -= amount
       accounts[target].balance += amount
   ```

   The `try` sits inside the loop so one bad transfer is logged and the rest still run.

   ```python
   def process_batch(batch, accounts):
       done, errors = 0, []
       for source, target, amount in batch:
           try:
               accounts[source].transfer(amount, target, accounts)
               done += 1
           except (InsufficientFunds, InvalidAccount) as exc:
               errors.append(f"{type(exc).__name__}: {exc}")
       return done, errors
   ```

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`. Press Done for the flag.

**Common mistakes.**

- In `retry`, printing `Retrying...` after the final failure too; the check expects exactly 2 prints for 3 attempts.
- Wrapping the whole `for` loop in one `try` in `process_batch`, so the first error stops the batch.
- Subtracting from the source before checking that the target exists, so money vanishes when `InvalidAccount` is raised and the final balances are wrong.
