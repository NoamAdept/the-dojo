# Pipeline Practice

What you will learn:

- how to read a CSV file,
- how to join grep, sort, head and cut with pipes,
- how to save the result in a file with >.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Goal
readings.csv has 3 columns: callsign,region,strength. List the 3
strongest callsigns in the north region.

## Deliverable
- **answer.txt**: 3 callsigns, 1 per line, strongest first.

## Tools

```
grep   sort   head   cut   ./check
```

## Steps
1. Press Start.
2. Keep only region=north. Sort by strength. Take the top 3 callsigns.
3. Write answer.txt. Then run:

```
./check
```

4. When the check passes, press Done.
