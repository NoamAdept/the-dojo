## Practicing Piping

*lls-piping · medium*

**Goal.** Write fifteen scripts that redirect stdin, stdout and stderr to files, filter streams with `grep`, `grep -v` and `sed`, split a stream with `tee` and process substitution, and pass data through a named pipe (FIFO).

**You need to know.**

- `>` writes stdout to a file, `>>` appends, `2>` redirects stderr, `<` feeds a file into stdin (README lesson).
- `2>&1` merges stderr into stdout, so it can go through a pipe.
- `tee FILE` copies a stream to a file and passes it on.
- `<(cmd)` and `>(cmd)` (process substitution) look like file names that connect to a program.
- `mkfifo NAME` makes a named pipe; `&` runs a command in the background and `wait` waits for it.

**Walkthrough.**

Scripts start in the home folder, so a plain file name lands in `~`. Every answer file starts with `#!/bin/bash`. `C` below stands for `$DOJO/challenge`, but write it out in full.

1. Tasks 1 to 5: redirections.

   ```bash
   echo PWN > COLLEGE                                        # task1.sh
   "$DOJO/challenge/run" > myflag                            # task2.sh
   "$DOJO/challenge/append" >> ~/the-flag                    # task3.sh
   "$DOJO/challenge/run" > myflag 2> instructions            # task4.sh
   ```

   Task 3 must append: `append` already wrote the first half of the file itself, and `>` would wipe it. In task 4, `>` takes stdout and `2>` takes stderr to separate files. `task5.sh` is two lines:

   ```bash
   echo COLLEGE > PWN
   "$DOJO/challenge/needinput" < PWN
   ```

2. Tasks 6 to 8: grep stored, live and error output.

   ```bash
   "$DOJO/challenge/noisy" > "$DOJO/tmp/data.txt"            # task6.sh, line 1
   grep "academy{" "$DOJO/tmp/data.txt"                      # task6.sh, line 2
   "$DOJO/challenge/noisy" | grep "academy{"                 # task7.sh
   "$DOJO/challenge/noisyerr" 2>&1 | grep "academy{"         # task8.sh
   ```

   A pipe only carries stdout, so task 8 needs `2>&1` before the `|` to send stderr along.

3. Tasks 9 and 10: remove the noise.

   ```bash
   "$DOJO/challenge/decoys" | grep -v DECOY                  # task9.sh
   "$DOJO/challenge/fakeflag" | sed "s/FAKEFLAG//g"          # task10.sh
   ```

   `grep -v` keeps lines that do NOT match. `s/FAKEFLAG//g` replaces every `FAKEFLAG` with nothing; `g` means all of them on the line.

4. Task 11: `tee` in the middle. First run `pwn` alone: it prints its usage, `pwn --secret SECRET_ARG`, and says the argument should be `pipeline7`.

   ```bash
   "$DOJO/challenge/pwn" --secret pipeline7 | tee ~/pwn.log | "$DOJO/challenge/college"
   ```

   `tee` saves a copy to `~/pwn.log` and passes the same lines on to `college`.

5. Task 12: compare two programs' outputs.

   ```bash
   diff <("$DOJO/challenge/print_decoys") <("$DOJO/challenge/print_decoys_and_flag")
   ```

   Each `<(...)` acts like a file holding that program's output, so `diff` shows only the extra line.

6. Task 13: one stdout, two readers.

   ```bash
   "$DOJO/challenge/hack" | tee >("$DOJO/challenge/the") | "$DOJO/challenge/planet"
   ```

   `tee` writes one copy into the `>(...)` "file" (which is `the`) and passes the other copy down the pipe to `planet`.

7. Task 14: stderr to one program, stdout to another.

   ```bash
   "$DOJO/challenge/hack" 2> >("$DOJO/challenge/the") | "$DOJO/challenge/planet"
   ```

   `2>` sends stderr into the process substitution, while the normal `|` carries stdout. Note the space between `2>` and `>(`.

8. Task 15: a named pipe.

   ```bash
   mkfifo "$DOJO/tmp/flag_fifo"
   "$DOJO/challenge/fifo" > "$DOJO/tmp/flag_fifo" &
   cat "$DOJO/tmp/flag_fifo"
   wait
   ```

   Opening a FIFO blocks until both a writer and a reader are there. So the writer runs in the background with `&`, `cat` reads in the foreground, and `wait` lets the writer finish.

9. Test with `./try N`, then `./check`.

**Check.** `./check` prints `15/15 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Writing `2>&1` after the pipe, or `cmd | grep x 2>&1`. The merge has to happen on the program that writes stderr, before the `|`.
- Running the FIFO writer in the foreground. The script then hangs forever (the check stops it after 8 seconds). Also, a second `./try 15` reports "File exists" from `mkfifo` in the practice copy; that does not affect `./check`.
- Using `>` instead of `>>` in task 3, which destroys the first half of the secret.
