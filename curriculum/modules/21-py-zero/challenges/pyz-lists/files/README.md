# Lists

**What you will learn:** how to keep many values together in one list, and how to work with them.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

Replace each `raise NotImplementedError` in `tasks.py`. Your functions must not change the list that they get.

1. **ends**: `ends(items)` returns a new list with only the first item and the last item. For example, `ends([4, 8, 15, 16])` returns `[4, 16]`.
2. **middle**: `middle(items)` returns everything except the first and last item. Use a slice.
3. **evens_up_to**: `evens_up_to(n)` returns a list of the even numbers from 0 up to `n`, including `n`. Build it with `append` in a loop. For example, `evens_up_to(7)` returns `[0, 2, 4, 6]`.
4. **count_above**: `count_above(items, limit)` returns how many items are greater than `limit`.
5. **average**: `average(items)` returns the average (the sum divided by the count) of a list of numbers. The list is never empty.
6. **squares**: `squares(n)` returns `[0, 1, 4, ..., (n-1)*(n-1)]`. Use a list comprehension.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
