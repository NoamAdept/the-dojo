## Environment

*orient-environment · medium*

**Goal.** Open the prepared lab shell, find the two environment variables that each hold half of the flag, join them in order, and submit the result.

**You need to know.**

- Environment variables are per-process settings that children inherit (README, "Lesson").
- `env`, `printenv`, and `grep` to filter them.
- `"${A}${B}"` joins two values with nothing in between.

**Walkthrough.**

1. Do not trust the files. `decoy.env` and the `DECOY_FLAG` line inside `lab_shell.sh` are fakes; `README_OPS.txt` says so ("If you only read files, you will find decoys").

2. Enter the lab shell.

   ```bash
   ./lab_shell.sh
   ```

   It loads the real parts from a hidden `.lab_env` file planted at Start, deletes that file, and opens a new bash. The parts now exist only in this shell's environment.

3. List the lab variables.

   ```bash
   printenv | grep '^LAB_'
   ```

   You see `LAB_SESSION`, `LAB_HINT` ("Parts may be split. Order matters."), `LAB_FLAG_PART1` and `LAB_FLAG_PART2`. `env | sort` shows the same list in a stable order.

4. Join the parts, PART1 first.

   ```bash
   printf '%s\n' "${LAB_FLAG_PART1}${LAB_FLAG_PART2}"
   ```

   Putting the two variables side by side in one string concatenates them, giving a complete `flag{...}`.

5. Copy it, leave the lab shell, and submit.

   ```bash
   exit
   academy submit 'flag{...}'
   ```

   Replace `flag{...}` with the line printed in step 4, or paste it in the dojo.

**Check.** The dojo accepts the joined value of `LAB_FLAG_PART1` and `LAB_FLAG_PART2`.

**Common mistakes.**

- Submitting `DECOY_FLAG` or the parts in `decoy.env`. Those are planted fakes.
- Copying the flag after typing `exit`: `.lab_env` is deleted on the first run, so `./lab_shell.sh` a second time says "Lab env missing". Copy it before exiting, or press Start again in the dojo.
- Joining in the wrong order (PART2 first) or adding a space between the parts.
