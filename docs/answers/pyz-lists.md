## Lists

*pyz-lists · easy*

**Goal.** Write six functions in `tasks.py` that index, slice, build and summarise lists, without changing the list they are given.

**You need to know.**

- Indexing from the front (`items[0]`) and the back (`items[-1]`).
- Slices like `items[1:-1]` make a new list (README lesson).
- `append` in a loop, and `sum` / `len`.
- List comprehensions: `[expression for x in something]`.

**Walkthrough.**

1. Open `tasks.py` and replace each `raise NotImplementedError`. The check also makes sure the input list is unchanged, so always build a new list.

2. Task 1: `ends`.

   ```python
   def ends(items):
       return [items[0], items[-1]]
   ```

   Square brackets make a new two-item list from the first and last items. For a one-item list both are the same item.

3. Task 2: `middle`.

   ```python
   def middle(items):
       return items[1:-1]
   ```

   The slice starts at index 1 and stops before the last item, and it returns a copy.

4. Task 3: `evens_up_to`.

   ```python
   def evens_up_to(n):
       result = []
       for i in range(0, n + 1, 2):
           result.append(i)
       return result
   ```

   A step of 2 from 0 gives only even numbers, and `n + 1` includes `n` when it is even.

5. Task 4: `count_above`.

   ```python
   def count_above(items, limit):
       count = 0
       for x in items:
           if x > limit:
               count += 1
       return count
   ```

   Loop over the items themselves and count the ones strictly greater than the limit; an empty list gives 0.

6. Task 5: `average`.

   ```python
   def average(items):
       return sum(items) / len(items)
   ```

   `sum` adds the items, `len` counts them, and `/` gives a float.

7. Task 6: `squares`, as a list comprehension.

   ```python
   def squares(n):
       return [i * i for i in range(n)]
   ```

   The comprehension builds the list in one line; `range(n)` stops at `n - 1`, as the task asks.

8. Run the check.

   ```bash
   ./check
   ```

**Check.** `./check` prints `6/6 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Changing the input, for example `items.pop(0)` in `middle`; the check reports "changed the list it was given".
- `range(0, n, 2)` in task 3, which drops `n` when `n` is even.
- Writing `squares` with `append` in a loop: the value is right, but the check wants a comprehension.
