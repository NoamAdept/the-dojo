## Shell Variables

*lls-variables · easy*

**Goal.** Write eight scripts that print, set, quote and export variables, filter `env`, store a command's output in a variable, and fill a variable with `read` from stdin and from a file.

**You need to know.**

- `NAME=value` with no spaces sets a variable; `$NAME` expands it (README lesson).
- Quotes keep a value with spaces in one piece.
- Only `export`ed variables reach programs you start; `env` lists those.
- `$(command)` captures a command's output; `read NAME` reads one line from stdin, and `< FILE` feeds a file to it.
- For tasks 2, 3, 4, 6, 7 and 8 the check runs your script and then looks at the variable values your shell ended with.

**Walkthrough.**

Every answer file starts with `#!/bin/bash`.

1. Task 1: print a variable the check sets.

   ```bash
   echo "$FLAG"
   ```

2. Task 2: set a variable.

   ```bash
   PWN=COLLEGE
   ```

   No spaces around `=`, otherwise bash tries to run a command called `PWN`.

3. Task 3: a value with a space.

   ```bash
   PWN="COLLEGE YEAH"
   ```

   Without quotes, bash would set `PWN=COLLEGE` just for one command and try to run `YEAH`.

4. Task 4: one exported, one not.

   ```bash
   export PWN=COLLEGE
   COLLEGE=PWN
   "$DOJO/challenge/run"
   ```

   `run` prints what it can see: `PWN=COLLEGE` (exported) and `COLLEGE=<unset>` (only a shell variable).

5. Task 5: only the `FLAG` line of `env`.

   ```bash
   env | grep "^FLAG="
   ```

   `^` anchors the match to the start of the line and the `=` ends the name, so `FLAGPOLE=` and `MYFLAG=` are skipped.

6. Task 6: store a command's output.

   ```bash
   PWN=$("$DOJO/challenge/secret")
   ```

   `$( )` runs the program and replaces itself with what the program printed.

7. Task 7: read from stdin.

   ```bash
   read PWN
   ```

   `read` takes one line from the input (the check sends `COLLEGE`) and stores it in `PWN`.

8. Task 8: read the first line of a file.

   ```bash
   read PWN < "$DOJO/challenge/read_me"
   ```

   `<` connects the file to `read`'s stdin, so it gets the file's first line.

9. Test with `./try N`, then `./check`.

**Check.** `./check` prints `8/8 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- `PWN = COLLEGE` with spaces. The result is `PWN: command not found`.
- Exporting both variables in task 4, or running `run` before the `export` line. `run` must see `PWN` but not `COLLEGE`.
- `env | grep FLAG` in task 5. It also prints the look-alike decoys.
