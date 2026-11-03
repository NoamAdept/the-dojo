# Follow the Stack

What you will learn:

- what the call stack is
- how to print it with backtrace
- how to read the frame numbers in the right order

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Goal
Stop at capture. Read a backtrace and write down the chain of calls.

## Deliverable
- **answer.txt**: outermost to innermost, like: main -> name -> capture

## Steps
1. Press Start, then: `./run`
2. GDB: break capture → run → backtrace (bt)
3. Write answer.txt, then: `./check`
4. Press Done when check passes.
