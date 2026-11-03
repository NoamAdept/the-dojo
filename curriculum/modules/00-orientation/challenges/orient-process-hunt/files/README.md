# Process Hunt

What you will learn:

- what a process and a PID are,
- how to find a process with ps,
- how to read its start command and its folder from /proc.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Goal
A helper process runs in the background. Find 5 facts about it. Write
them into report.txt. Then prove them with `./check`.

## Tools

```
./run   ps   cat   /proc   ./check
```

## Steps
1. Press Start in the dojo. Then start the helper:

```
./run
```

2. Find its process ID (PID):

```
ps aux | grep helper
```

   On a shared lab machine you may see other learners' helpers too. Yours is the one
   whose folder (step 3) is your challenge folder.

3. Look in /proc/<PID>/. Find the full start command and the working
   directory (folder). LESSON.md shows the exact commands.
4. In the start command, find --notes /some/path/note.txt. Open that
   file. Copy the secret_code value.

5. Fill in every line in report.txt. Use report.template to see the
   shape. Then run:

```
./check
```

6. When the check passes, press Done in the dojo.
