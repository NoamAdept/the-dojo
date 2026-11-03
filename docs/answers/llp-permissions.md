## File Permissions

*llp-permissions · medium*

**Goal.** Fill in `answers/task1.sh` to `answers/task7.sh` to read modes, change them with symbolic and octal `chmod`, use the execute bit, `umask`, find setuid files and change a file's group. `./check` creates the files with fresh permissions on every run.

**You need to know.**

- The `rwx` triplets for user, group and other, and their octal values (r=4, w=2, x=1).
- `chmod g+w,o-rwx` (symbolic) versus `chmod 750` (octal).
- `umask` removes bits from new files (base 666) and new folders (base 777).
- `find -perm -o=r` and `find -perm -4000` (setuid), `-printf '%f\n'` for the bare name.
- `chgrp GROUP FILE` works only for a group you belong to.

**Walkthrough.**

Remove the `# TODO` line from every file before running `./check`.

1. Task 1, files in `box/` that others may read.

   ```bash
   #!/bin/bash
   find box -type f -perm -o=r -printf '%f\n' | sort
   ```

   `-perm -o=r` means "at least the other-read bit is set", `%f` prints the name without `box/`, and `sort` gives the required order.

2. Task 2, symbolic chmod on `notes.txt`.

   ```bash
   #!/bin/bash
   chmod g+w,o-rwx notes.txt
   ```

   Symbolic mode changes only the bits you name, so the owner bits stay exactly as they were.

3. Task 3, octal chmod.

   ```bash
   #!/bin/bash
   chmod 600 secret.txt
   chmod 750 run.sh
   ```

   `600` is `rw-------` and `750` is `rwxr-x---`; octal sets all nine bits at once.

4. Task 4, execute bit.

   ```bash
   #!/bin/bash
   chmod u+x hello.sh
   ./hello.sh
   ```

   `./hello.sh` only runs once the owner has `x`; the checker looks for the script's output too.

5. Task 5, umask.

   ```bash
   #!/bin/bash
   umask 027
   touch private.log
   mkdir logs
   ```

   `027` removes write from group and everything from other: 666 becomes 640 for the file and 777 becomes 750 for the folder. The checker requires the word `umask` in the script.

6. Task 6, setuid files in `bin/`.

   ```bash
   #!/bin/bash
   find bin -type f -perm -4000 -printf '%f\n' | sort
   ```

   `4000` is the setuid bit (the `s` in `rws`), and `-perm -4000` matches files that have it plus anything else.

7. Task 7, chgrp.

   ```bash
   #!/bin/bash
   chgrp "$(cat group.txt)" shared.txt
   ```

   The group name comes from the file, and the checker picks one of your own groups so no `sudo` is needed.

8. Run the checker.

   ```bash
   ./check
   ```

**Check.** `./check` prints `7/7 tasks pass` and then `CHECK_OK`. Then press Done.

**Common mistakes.**

- Using `chmod 770 notes.txt` in task 2: octal overwrites the owner bits, which the task says to keep.
- Using `-perm 4000` (no dash) in task 6: that means "exactly 4000" and matches nothing useful.
- Doing task 5 with `chmod` afterwards: the checker rejects a script without `umask`.
