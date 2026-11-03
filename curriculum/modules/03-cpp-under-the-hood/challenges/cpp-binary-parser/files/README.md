# Parse Length-Prefixed Records

**What you will learn:**

- how a stream of type/length/payload records is laid out in memory
- how to walk along it with an offset
- how to call a callback that you were given
- how to never read past the end of a buffer
- how to write a callback of your own

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

Fill in `records.cpp`. Do not change `records.hpp`. `parse_records` has one `// TODO task N` line for task 1 and one for task 2. Delete each line when you do that part.

1. **Walk the records**: the input may be well-formed (correct and complete). Then `parse_records(data, size, visit, context)` calls `visit(type, payload, length, context)` once for each record, in order. Then it returns `true`. An empty buffer (size 0) returns `true` and does not call `visit`. Payloads with length 0 are fine.
2. **Refuse truncated input**: the buffer may end inside a header or a payload. Then return `false`. Do not read past the end. Do not call `visit` for the broken record. (Complete records before it may already have been visited. That is fine.)
3. **Your own visitor**: `count_records(data, size)` returns how many complete records the buffer holds. It returns `-1` when the buffer is truncated. Write a small visitor function that counts through its `void*` context. Let `parse_records` do the walking.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
