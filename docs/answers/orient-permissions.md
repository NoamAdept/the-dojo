## Permissions

*orient-permissions · easy*

**Goal.** `vault/flag.txt` has mode `----------`, so even its owner cannot read it. Give yourself read permission with `chmod`, read the flag and submit it.

**You need to know.**

- How to read the ten mode characters from `ls -l` (README, "Lesson").
- `u`, `g`, `o` and `r`, `w`, `x`, plus `+` to add and `-` to remove.
- The owner may always change a file's mode, no `sudo` needed.

**Walkthrough.**

1. Inspect the vault.

   ```bash
   ls -l vault
   whoami
   ```

   `flag.txt` shows `----------` (no permission for anyone) and `memo.txt` shows `-rw-r--r--`. The owner column matches your `whoami`, so you are allowed to fix it.

2. Confirm you are blocked.

   ```bash
   cat vault/flag.txt
   ```

   This prints `Permission denied` because the user `r` bit is missing.

3. Add read permission for the owner only.

   ```bash
   chmod u+r vault/flag.txt
   ls -l vault/flag.txt
   ```

   `u+r` adds just the owner read bit; the mode becomes `-r--------` (octal `400`). The helper `sh check_perms.sh` prints the same thing with `stat`.

4. Read the flag.

   ```bash
   cat vault/flag.txt
   ```

5. Submit it: paste it in the dojo, or put it in the flag file and submit.

   ```bash
   cat vault/flag.txt > "$(cat .flagpath 2>/dev/null || echo $HOME/flag.txt)"
   academy submit
   ```

   `.flagpath` tells you where the academy expects the flag file; if it is missing the command falls back to `~/flag.txt`.

**Check.** The dojo accepts the flag printed by `cat vault/flag.txt`. Optional extension: the file stays at `400` (`stat -c '%a' vault/flag.txt` prints `400`), so group and other still cannot read it.

**Common mistakes.**

- Using `sudo cat` or `chmod 777`. Both "work" but skip the lesson; the README says not to use sudo, and 777 opens the file to everyone.
- Running `chmod u+r vault` (the folder) instead of `vault/flag.txt`.
- An instructor testing as root will not see "Permission denied", because root ignores mode bits. Test as a normal user.
