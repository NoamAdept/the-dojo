## Pondering Paths

*lls-paths · easy*

**Goal.** Write eight scripts that run small programs under `$DOJO` by absolute paths, by relative paths (with and without `.`), from specific working directories, and finally with a `~/` argument.

**You need to know.**

- Absolute paths start with `/` and work from anywhere; relative paths start at the working directory (README, paths).
- `cd` in a script changes the directory for every line after it.
- `.` is the current folder; `./prog` runs a program from here because `PATH` does not include `.`.
- A leading `~` expands to `$HOME`.
- The test programs print `RAN argv0=...` and `RAN cwd=...` lines, so the check sees exactly how you ran them.

**Walkthrough.**

Run `. ./env.sh` once to try commands by hand. Every answer file starts with `#!/bin/bash`.

1. Task 1: the root, by absolute path.

   ```bash
   "$DOJO/pwn"
   ```

   `$DOJO` expands to an absolute path, so the program name starts with `/`. Quotes guard against spaces.

2. Task 2: same idea, deeper.

   ```bash
   "$DOJO/challenge/run"
   ```

3. Task 3: run from a given working directory.

   ```bash
   cd "$DOJO/var/lib/academy"
   "$DOJO/challenge/position"
   ```

   `cd` sets the working directory first; the absolute path still finds the program.

4. Task 4: five places, in order.

   ```bash
   cd "$DOJO/etc"
   "$DOJO/challenge/tour"
   cd "$DOJO/usr/share"
   "$DOJO/challenge/tour"
   cd "$DOJO/var/log"
   "$DOJO/challenge/tour"
   cd "$DOJO/home"
   "$DOJO/challenge/tour"
   cd "$DOJO/tmp"
   "$DOJO/challenge/tour"
   ```

   Each `cd` changes where the next `tour` runs. The order must match the task.

5. Task 5: implicit relative path.

   ```bash
   cd "$DOJO"
   challenge/run
   ```

   A name containing a `/` is treated as a path, so bash runs `challenge/run` relative to `$DOJO` without searching `PATH`.

6. Task 6: explicit relative path with `.`.

   ```bash
   cd "$DOJO"
   ./challenge/run
   ```

7. Task 7: a program in the current folder.

   ```bash
   cd "$DOJO/challenge"
   ./run
   ```

   A bare `run` would be searched in `PATH` and not found; `./run` points at this folder.

8. Task 8: home sweet home.

   ```bash
   "$DOJO/challenge/copyflag" ~/f
   ```

   You type three characters, `~/f`. Bash expands it to `$HOME/f`, an absolute path inside the home folder, which is what `copyflag` demands. It writes the secret there.

9. Test each with `./try N`, then `./check`.

**Check.** `./check` prints `8/8 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Writing `"~/f"` in quotes. Quotes stop `~` expansion, so `copyflag` gets a relative path and refuses.
- Typing the full expanded path in tasks 5 to 7. The check looks at exactly how the program was called (`challenge/run`, a path with `.`, `./run`).
- Forgetting the `cd` line, so the program runs in the home folder and the check reports the wrong `cwd`.
