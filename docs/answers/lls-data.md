## Data Manipulation

*lls-data · easy*

**Goal.** Write six one-line pipelines that clean up a program's output with `tr`, `head`, `cut` and `sort` so that only the secret (or the right input) comes out.

**You need to know.**

- `tr SET1 SET2` maps characters; `tr -d SET` deletes them (README lesson).
- `head -n N` keeps the first N lines, `tail -n N` the last N.
- `cut -d " " -f 2` keeps the second space-separated field.
- `sort` orders lines alphabetically; `|` sends one program's output into the next.
- Run each program alone first, then add one filter at a time.

**Walkthrough.**

All programs are in `$DOJO/challenge/`. Every answer file starts with `#!/bin/bash`.

1. Task 1: swap the case back.

   ```bash
   "$DOJO/challenge/swapcase" | tr a-zA-Z A-Za-z
   ```

   Each lower-case letter maps to its upper-case partner and the other way round, which undoes the swap.

2. Task 2: delete the noise characters.

   ```bash
   "$DOJO/challenge/carets" | tr -d "^%"
   ```

   `-d` removes every character listed in the set. The quotes keep the shell away from `^` and `%`.

3. Task 3: join the broken lines.

   ```bash
   "$DOJO/challenge/newlines" | tr -d "\n"
   ```

   `"\n"` is the newline character, so `tr -d` glues all lines together.

4. Task 4: only the first 7 lines reach `college`.

   ```bash
   "$DOJO/challenge/pwn" | head -n 7 | "$DOJO/challenge/college"
   ```

   Two pipes, three commands: `head` sits in the middle and passes on just 7 lines.

5. Task 5: pick the second column and join it.

   ```bash
   "$DOJO/challenge/columns" | cut -d " " -f 2 | tr -d "\n"
   ```

   `cut` keeps one character per line; `tr -d "\n"` then puts them on a single line.

6. Task 6: the line that sorts last.

   ```bash
   sort "$DOJO/challenge/flags.txt" | tail -n 1
   ```

   After sorting, the real secret is the final line, and `tail -n 1` keeps only that one. `sort -r FILE | head -n 1` works too.

7. Test with `./try N`, then `./check`.

**Check.** `./check` prints `6/6 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Writing `tr -d \n` without quotes. The shell turns `\n` into a plain `n`, so `tr` deletes the letter n instead of newlines.
- Using `cut -f 2` without `-d " "`. `cut` splits on tabs by default and prints the whole line.
- Printing `head -n 7` to the screen in task 4 instead of piping it into `college`.
