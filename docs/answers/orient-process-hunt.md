## Process Hunt

*orient-process-hunt · medium*

**Goal.** `./run` starts a hidden background helper. Find its PID, its full start command, its working folder, the notes file named in its command, and the secret code inside that file. Write all five into `report.txt` and run `./check`.

**You need to know.**

- A process, a PID, and background programs (README, "Lesson").
- `ps aux | grep NAME` and `pgrep -f PATTERN`.
- `/proc/PID/cmdline` (words separated by zero bytes) and `/proc/PID/cwd` (a link).
- `key=value` lines in a text file, edited with `vim`.

**Walkthrough.**

1. Start the helper.

   ```bash
   ./run
   ```

   It prints that a helper started but hides the PID on purpose.

2. Find the PID.

   ```bash
   ps aux | grep helper
   pgrep -f 'helper --work'
   ```

   In `ps` the PID is column 2 (ignore the line for your own `grep`). `pgrep -f` prints only the number.

3. Read the full command. Replace `PID` with the number.

   ```bash
   tr '\0' ' ' < /proc/PID/cmdline ; echo
   ```

   The words in `cmdline` are separated by zero bytes; `tr` turns them into spaces. It looks like `helper --work --notes /tmp/academy_note_NNNNNNNN/note.txt`.

4. Read the working folder.

   ```bash
   readlink /proc/PID/cwd
   ```

   `cwd` is a link to the folder the process stands in. It is the challenge folder, because `./run` was started from there.

5. Open the notes file named after `--notes` and copy the code.

   ```bash
   cat /tmp/academy_note_NNNNNNNN/note.txt
   ```

   The line `secret_code=CODE-XXXXXXXX` holds the answer; use only the part after `=`.

6. Fill in the report (`vim report.txt`, press `i` to type, then `Esc` and `:wq` Enter to save and quit):

   ```text
   process_number=4839
   full_command=helper --work --notes /tmp/academy_note_94351217/note.txt
   folder=/home/student/orient-process-hunt
   notes_file=/tmp/academy_note_94351217/note.txt
   secret_code=CODE-5911FD71
   ```

   These values are from one test run; every `./run` makes a new PID, path and code. The checker compares each line against the live process.

7. Run the checker.

   ```bash
   ./check
   ```

   On success it writes the flag into the flag file (usually `/home/flag.txt`, or the path in `.flagpath`). Then `cat` that file and run `academy submit`, or press Done.

**Check.** `./check` prints `Correct! All answers match the running process.` and `CHECK_OK`.

**Common mistakes.**

- Running `./run` again after writing the report: it kills the old helper and makes a new PID, notes path and code, so every answer is now wrong. Re-read everything after each `./run`.
- Copying the PID of the `grep helper` line instead of the helper.
- Writing `secret_code=secret_code=CODE-...` or leaving a line blank. All five lines are required.
