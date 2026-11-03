# Log Detective

What you will learn:

- how to read a structured log,
- how to cut 1 field out of each line,
- how to count repeated lines with sort and uniq -c,
- how to change the shape of lines with awk.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Goal
Count the WARN lines in receiver.log for each component. Write the result
in report.txt.

## Deliverable
- **report.txt**: 1 line for each component, in alphabetical order. Each line has the shape `component=count`.
- Count only `level=WARN` lines (example: `audio=2`).

## Steps
1. Press Start. Open this folder.
2. Look at receiver.log. grep, cut, sort and uniq can help.
3. Write report.txt. Then run:

```
./check
```

4. When the check passes, press Done in the dojo.
