# Automate an Investigation

What you will learn:

- how to read a CSV table with csv.DictReader
- how to filter and group its rows with a dictionary of lists
- how to save the result as JSON

Then you can repeat the same analysis on any new data file.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Goal
Complete investigate(input_path, output_path).

## Rules

```
Use only LOCKED rows.
Keep stations with at least 3 LOCKED rows.
For each: count and average_snr (one decimal).
Write JSON with station keys sorted.
```

## Steps
1. Press Start and open the starter file.
2. Write investigate. Then run `./check`.
3. Press Done when check passes.
