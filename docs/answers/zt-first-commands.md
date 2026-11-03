## Your First Commands

*zt-first-commands · easy*

**Goal.** Run the first few commands (`echo`, `whoami`, `date`) and save what they print into four files: `hello.txt`, `me.txt`, `today.txt` and `list.txt`.

**You need to know.**

- The prompt ends in `$`; you type what comes after it, never the `$` itself (README, "The terminal and the shell").
- A line is a command plus arguments, split at spaces (README, "Commands and arguments").
- `>` sends output into a file and replaces it; `>>` adds to the end (README, "Saving output into a file").
- `ls` lists files, `cat NAME` prints one.

**Walkthrough.**

Work in the challenge folder, where the terminal opens.

1. Task 1: make `hello.txt`.

   ```bash
   echo Hello terminal > hello.txt
   cat hello.txt
   ```

   `echo` prints its two arguments back, and `>` catches that text and writes it into `hello.txt` instead of the screen. `cat` lets the learner see it worked.

2. Task 2: save your user name.

   ```bash
   whoami > me.txt
   ```

   Same pattern as task 1, only the command in front of `>` is `whoami`. The check accepts any real account name on the machine.

3. Task 3: save the date.

   ```bash
   date > today.txt
   ```

   The check only looks for a year and a time like `14:03`, which every `date` output has.

4. Task 4: a file with two lines.

   ```bash
   echo first > list.txt
   echo second >> list.txt
   cat list.txt
   ```

   The single `>` creates the file with `first`; the double `>>` appends `second` as a new line below it.

5. Run the checker.

   ```bash
   ./check
   ```

**Check.** `./check` prints `4/4 tasks pass` and then `CHECK_OK`. The learner then presses Done.

**Common mistakes.**

- Typing the `$` from the examples, or writing `Echo` with a capital E. The shell then says "command not found".
- Using `>` twice in task 4. The second command replaces the file, so it only holds `second`. Fix: run both commands again, `>` first, then `>>`.
- Typing their own name into `me.txt` by hand (`echo Noam > me.txt`). The check wants the real account name, so let `whoami` write it.
