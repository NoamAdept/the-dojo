# Classify Signal Strengths

What you will learn:

- how to turn a rule like "below 5 is weak" into an if/elif/else chain
- how to count results in a dictionary
- how one Python file can be a program you run and also a toolbox that
  `./check` imports

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Goal
Complete classify.py. Write two functions: classify_signal(snr) and summarize(values).

## Rules

```
weak:   snr < 5
usable: 5 <= snr <= 14
strong: snr >= 15
```

summarize returns a dict (dictionary) with a count for each label.

## Steps
1. Press Start and open classify.py.
2. Try: `python3 classify.py 2 8 19`
3. Prove: `./check`
4. Press Done when check passes.
