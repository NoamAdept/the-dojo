## Chaining Commands and Scripts

*llp-chaining · easy*

**Goal.** Fill in `answers/task1.sh` to `answers/task7.sh`: three one-line chains with `;`, `&&` and `||`, three small scripts that use arguments and `if`, and one script that writes an executable `./hello`.

**You need to know.**

- `;` always runs the next command, `&&` only after success, `||` only after failure.
- `$1`, `$2` are arguments and `$#` counts them.
- `if [ -f "$1" ]`, `-lt`, `-eq`, `elif`, `exit 1`.
- A shebang line plus `chmod +x` lets a file run as `./name`.
- A quoted heredoc (`<<'EOF'`) writes text without expanding `$1`.

**Walkthrough.**

`./check` runs each script in a folder that already holds the helper programs (`./first`, `./build`, and so on). Remove the `# TODO` line in every file, or the checker counts the task as unfinished.

1. Task 1, semicolon.

   ```bash
   #!/bin/bash
   ./first ; ./second
   ```

   `;` ignores the exit code, so `./second` runs either way.

2. Task 2, success only.

   ```bash
   #!/bin/bash
   ./build && ./deploy
   ```

   `&&` runs the right side only when the left side exited with 0.

3. Task 3, fallback.

   ```bash
   #!/bin/bash
   ./primary || ./backup
   ```

   `||` runs the right side only when the left side failed (non-zero exit).

4. Task 4, arguments.

   ```bash
   #!/bin/bash
   echo "$2 $1"
   echo "$#"
   ```

   `$2 $1` swaps the first two arguments and `$#` is the argument count, so `x y z` gives `y x` then `3`.

5. Task 5, if / else.

   ```bash
   #!/bin/bash
   if [ -f "$1" ]; then
       echo "found $1"
   else
       echo "missing $1"
       exit 1
   fi
   ```

   `-f` is true only for a regular file (a folder counts as missing), and `exit 1` sets the failure code the task asks for.

6. Task 6, elif.

   ```bash
   #!/bin/bash
   if [ "$1" -lt 0 ]; then
       echo negative
   elif [ "$1" -eq 0 ]; then
       echo zero
   elif [ "$1" -lt 10 ]; then
       echo small
   else
       echo large
   fi
   ```

   The tests run top to bottom and the first true one wins, so by the third test the number is already known to be 1 or more.

7. Task 7, shebang. The script must create `hello`, not be `hello`.

   ```bash
   #!/bin/bash
   cat > hello <<'EOF'
   #!/bin/bash
   echo "Hello, $1!"
   EOF
   chmod +x hello
   ```

   The quotes around `'EOF'` keep `$1` literal inside `hello`, and `chmod +x` lets `./check` run `./hello Ada` directly.

8. Run the checker.

   ```bash
   ./check
   ```

**Check.** `./check` prints `7/7 tasks pass` and then `CHECK_OK`. Then press Done.

**Common mistakes.**

- Writing `<<EOF` without quotes in task 7: `$1` is expanded while writing the file (to nothing), so `hello` always prints `Hello, !`.
- Using `-e` instead of `-f` in task 5, which also accepts folders.
- Comparing numbers with `<` or `>` inside `[ ]`: those are redirections there, not comparisons. Use `-lt` and `-eq`.
