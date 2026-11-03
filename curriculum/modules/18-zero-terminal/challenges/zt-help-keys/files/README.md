# Getting Help and Handy Keys

**What you will learn:**

- how to ask a command for help
- what options are
- the keys that save you the most typing: Tab, the up arrow, and Ctrl-C

New to this? Read **LESSON.md** first. You can also press **Lesson** in the app.

## Your tasks

Tasks 1 to 3 are scripts in `answers/`, like last time. You do task 4 by hand.

1. **Count lines**: use `wc --help` to find the option that counts lines. `answers/task1.sh` prints the number of lines in `$DOJO/log.txt`. It may print the file name after the number. That is fine. It must print nothing else.
2. **Just the year**: use `date --help` to find the format piece for the year with the century (like 2026). `answers/task2.sh` prints only the current year.
3. **Let Tab type it**: in `$DOJO/signals/` there is a file whose name starts with `a-really`. `answers/task3.sh` prints the contents of that file. In your terminal, run `. ./env.sh` first. Then use Tab completion to get the long name right. Then put the command in the script.
4. **Stop it, twice**: run `./forever`. Stop it with Ctrl-C. Then press the up arrow and Enter to run it again. Stop it again with Ctrl-C. (Each Ctrl-C adds a line to `stopped.txt`.)

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
