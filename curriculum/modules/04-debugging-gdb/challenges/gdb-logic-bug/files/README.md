# Find a Logic Bug

What you will learn:

- how to stop on a line that you choose
- how to step 1 line at a time with next
- how to watch values with display
- how && (and) and || (or) really work in a range check

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Goal
A sample is usable when 10 <= sample <= 20. The loop is wrong. Fix target.cpp so it prints usable=4.

## Steps
1. Press Start, then: `./run`
2. In GDB, break near the if, then run. Display i and samples[i]. Step through the loop.
3. Fix the condition/loop in target.cpp
4. Prove it: `./check`, then Press Done
