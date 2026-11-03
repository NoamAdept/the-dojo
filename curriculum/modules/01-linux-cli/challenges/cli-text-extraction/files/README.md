# Text Extraction

What you will learn:

- how to describe a shape of text with a regular expression,
- how to take out only the matching parts with grep -oE,
- how to sort numbers and remove repeated ones.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Goal
Take every decimal MHz frequency out of bulletin.txt.

## Deliverable
- **frequencies.txt**: only unique numbers (no "MHz"), 1 per line, in numeric order.

## Steps
1. Press Start and read bulletin.txt.
2. Take out the numbers. grep -oE, sort -n and uniq can help.
3. Write frequencies.txt. Then run:

```
./check
```

4. When the check passes, press Done.
