## Variables, Quotes and the Practice Dojo

*zt-variables-dojo · easy*

**Goal.** Write five one- or two-line scripts in `answers/` that print a variable, set and use your own variable, and read and write files under `$DOJO`, including a path with a space in it.

**You need to know.**

- `NAME=value` sets a variable (no spaces around `=`); `$NAME` uses it (README lesson on variables).
- Double quotes keep text with spaces in one piece and still expand `$NAME`.
- `. ./env.sh` sets `DOJO` in your own shell so you can try commands by hand.
- `./try N` runs a script with the practice `DOJO`; `./check` uses its own dojo with different contents.

**Walkthrough.**

1. Set up the practice environment once.

   ```bash
   . ./env.sh            # DOJO is now .../dojo
   cat "$DOJO/message.txt"
   ```

   The leading `.` runs the file inside the current shell, so `DOJO` stays set afterwards.

2. Task 1: print `HOME`. In `answers/task1.sh`:

   ```bash
   #!/bin/bash
   echo "$HOME"
   ```

   The shell replaces `$HOME` with its value before `echo` runs. The check sets its own `HOME`, so typing a fixed path would fail.

3. Task 2: your own variable. In `answers/task2.sh`:

   ```bash
   #!/bin/bash
   band=fm
   echo "listening on $band"
   ```

   The first line stores `fm` in `band`; the second line expands it inside the double quotes. The check also reads the file and wants `band=fm` and `$band` in it.

4. Task 3: read from the dojo. In `answers/task3.sh`:

   ```bash
   #!/bin/bash
   cat "$DOJO/message.txt"
   ```

   The check writes a different message there, so the script must read the file, not echo the practice text.

5. Task 4: write into the dojo. In `answers/task4.sh`:

   ```bash
   #!/bin/bash
   echo done > "$DOJO/tmp/finished.txt"
   ```

   `>` creates the file at that path; the `tmp` folder already exists in the dojo.

6. Task 5: a path with a space. In `answers/task5.sh`:

   ```bash
   #!/bin/bash
   cat "$DOJO/my notes/today.txt"
   ```

   One pair of double quotes around the whole path keeps `my notes` as one argument.

7. Test each with `./try 1` to `./try 5`, then run `./check`.

**Check.** `./check` prints `5/5 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- `band = fm` with spaces. Bash then tries to run a command called `band` and says `band: command not found`.
- Leaving out the quotes in task 5. `cat` gets two arguments, `.../my` and `notes/today.txt`, and complains twice with `No such file or directory`.
- Using single quotes (`'$HOME'`). Single quotes stop expansion, so the script prints the text `$HOME`.
