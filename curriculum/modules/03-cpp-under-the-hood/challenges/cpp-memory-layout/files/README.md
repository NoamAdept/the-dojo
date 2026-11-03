# Decode a Header from Raw Bytes

**What you will learn:**

- how data arrives as a raw buffer of bytes
- how letters are stored as bytes
- how to see the byte order of your own computer
- why you decode field by field, and do not cast bytes to a struct
- how to refuse bad input before you read it

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

Write `decode_header` in `layout.cpp`, step by step. Do not change `layout.hpp`. Do not cast `data` to a `header*`. The function has one `// TODO task N` line for each task. Delete each line when you do that part.

1. **Refuse bad input**: return `false` in any of these cases:
   - `data` is `nullptr`
   - `out` is `nullptr`
   - `size` is less than 6

   In these cases, do not read any byte, and do not change `*out`.
2. **Single bytes**: copy `tag[0]`, `tag[1]`, `flags` and `length` from bytes 0, 1, 4 and 5 into `*out`. Then return `true`.
3. **Little-endian sequence**: build `sequence` from byte 2 (low) and byte 3 (high).

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
