## Getting Help and Handy Keys

*zt-help-keys · easy*

**Goal.** Use `--help` to find the right options for `wc` and `date`, use Tab completion to type a long file name, and stop a running program with Ctrl-C twice.

**You need to know.**

- `COMMAND --help` lists a command's options (README lesson on getting help).
- Tab completes file names; the up arrow recalls the last command.
- Ctrl-C interrupts the program that is running.
- `. ./env.sh` and `./try N`, as in the previous challenge.

**Walkthrough.**

1. Set up and read the help pages.

   ```bash
   . ./env.sh
   wc --help             # look for "lines": -l, --lines
   date --help           # look for "year": %Y
   ```

2. Task 1: count lines. Try it by hand first, then put it in `answers/task1.sh`:

   ```bash
   #!/bin/bash
   wc -l "$DOJO/log.txt"
   ```

   `-l` makes `wc` print only the line count (23 for the practice file), followed by the file name, which the check allows. The check uses a log of a different length.

3. Task 2: just the year. In `answers/task2.sh`:

   ```bash
   #!/bin/bash
   date +%Y
   ```

   A `+` argument tells `date` to use your own format, and `%Y` is the four-digit year.

4. Task 3: let Tab type it. At the prompt type `cat "$DOJO/signals/a` and press Tab. Bash fills in the rest. Add the closing `"` and press Enter to see the practice text. Then copy that line into `answers/task3.sh`:

   ```bash
   #!/bin/bash
   cat "$DOJO/signals/a-really-long-file-name-made-for-tab-completion-q7.txt"
   ```

5. Test tasks 1 to 3 with `./try 1`, `./try 2`, `./try 3`.

6. Task 4: done by hand, in the challenge folder.

   ```bash
   ./forever
   ```

   Press Ctrl-C. It prints `stopped with Ctrl-C` and writes that line into `stopped.txt`. Now press the up arrow, then Enter, and press Ctrl-C again. `stopped.txt` now has two lines.

7. Run `./check`.

**Check.** `./check` prints `4/4 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Plain `wc "$DOJO/log.txt"`. It prints three numbers (lines, words, bytes), and the check wants only one.
- `date +%y` (small y). That gives `26`, not `2026`.
- Stopping `./forever` with Ctrl-Z instead of Ctrl-C. Ctrl-Z only pauses it, so nothing is written to `stopped.txt`. Type `fg` and then press Ctrl-C.
