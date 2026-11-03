## Users and Groups

*llp-users · easy*

**Goal.** Fill in `answers/task1.sh` to `answers/task6.sh`: three scripts that report who you are, and three that read an `/etc/passwd`-style file and pick out shells, human accounts and extra root accounts.

**You need to know.**

- `whoami`, `id -u`, `id -g`, `id -Gn` (README, top section).
- The 7 colon-separated fields of a passwd line: name, password, UID, GID, comment, home, shell.
- `awk -F:` splits on colons; `$1` is the name, `$3` the UID, `$7` the shell.
- `sort -k2,2n` sorts numerically on column 2.

**Walkthrough.**

Replace the `# TODO` line in each file. `./check` rejects any file that still contains `TODO`, and for tasks 4 to 6 it feeds your script freshly generated `passwd.txt` files, so never hard-code names.

1. Task 1, your user name.

   ```bash
   #!/bin/bash
   whoami
   ```

   `whoami` prints the name that matches your current UID.

2. Task 2, UID and primary GID on one line.

   ```bash
   #!/bin/bash
   echo "$(id -u) $(id -g)"
   ```

   Each `$(...)` is replaced by the command's output, and `echo` joins them with one space.

3. Task 3, all your group names, one per line.

   ```bash
   #!/bin/bash
   id -Gn | tr ' ' '\n'
   ```

   `id -Gn` prints the names on one line separated by spaces, and `tr` turns each space into a newline.

4. Task 4, accounts whose shell is exactly `/bin/bash`, in file order.

   ```bash
   #!/bin/bash
   awk -F: '$7 == "/bin/bash" {print $1}' passwd.txt
   ```

   `==` compares the whole shell field, so `/bin/sh` and `/usr/bin/bash` do not slip in. On the sample file this prints root, sysadm, sdrd, barbara, margaret.

5. Task 5, human accounts (UID 1000 or more, not nobody), sorted by UID.

   ```bash
   #!/bin/bash
   awk -F: '$3 >= 1000 && $3 != 65534 {print $1, $3}' passwd.txt | sort -k2,2n
   ```

   awk compares `$3` as a number, the comma in `print` puts a space between name and UID, and `sort -k2,2n` orders on the UID column as numbers. On the sample: `barbara 1000`, `margaret 1002`, `edsger 1004`.

6. Task 6, every account with UID 0.

   ```bash
   #!/bin/bash
   awk -F: '$3 == 0 {print $1}' passwd.txt
   ```

   Any UID 0 account is root under another name; on the sample this finds `root` and the hidden `sysadm`.

7. Run the checker.

   ```bash
   ./check
   ```

**Check.** `./check` prints `6/6 tasks pass` and then `CHECK_OK`. Then press Done.

**Common mistakes.**

- Using `grep bash passwd.txt`: it also matches names or homes containing "bash" and shells like `/usr/bin/bash`.
- Sorting task 5 with plain `sort` (text order puts `10000` before `2000`) or forgetting to exclude `nobody`.
- Hard-coding `root` and `sysadm` for task 6; the checker uses different files.
