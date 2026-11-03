## Comprehending Commands

*lls-commands · easy*

**Goal.** Write fifteen short scripts that read files (`cat`, `grep`, `diff`), list them (`ls`, `ls -a`, `find`) and change the filesystem (`touch`, `rm`, `mv`, `cp`, `mkdir`, `ln -s`), all inside the fake filesystem `$DOJO`.

**You need to know.**

- The command table in the README (one line per command, with an example).
- `$DOJO` is the fake root; during the check `~` is `$DOJO/home/hacker`. Always quote `"$DOJO/..."`.
- The check uses its own secrets and random names, so scripts must read or search, never paste an answer.
- `. ./env.sh` to explore by hand, `./try N` to run one answer.

**Walkthrough.**

Every answer file starts with `#!/bin/bash`. The lines below go under it.

1. Tasks 1 to 3: `cat`, with `~` and absolute paths.

   ```bash
   cat ~/flag                               # task1.sh
   cat "$DOJO/flag"                         # task2.sh
   cat "$DOJO/opt/vault/a1/b2/c3/flag"      # task3.sh
   ```

   Tasks 2 and 3 are started from an unrelated folder, so only absolute paths work there.

2. Task 4: `grep` for the one real line among 20,000.

   ```bash
   grep "academy{" "$DOJO/challenge/data.txt"
   ```

   `grep` prints only lines containing the pattern. Quotes stop the shell from treating `{` specially.

3. Task 5: `diff` shows only the extra line.

   ```bash
   diff "$DOJO/challenge/decoys_only.txt" "$DOJO/challenge/decoys_and_real.txt"
   ```

   `diff` prints just the lines that differ (marked with `>`), not the shared decoys.

4. Tasks 6 and 11: listing.

   ```bash
   ls "$DOJO/challenge"                     # task6.sh
   ls -a "$DOJO"                            # task11.sh
   ```

   `-a` also shows names starting with `.`, which `ls` hides by default.

5. Tasks 7 to 10: create, delete, move, copy.

   ```bash
   touch "$DOJO/tmp/pwn" "$DOJO/tmp/college"           # task7.sh
   rm ~/delete_me                                      # task8.sh
   mv "$DOJO/flag" "$DOJO/tmp/hack-the-planet"         # task9.sh
   cp "$DOJO/flag" "$DOJO/tmp/hack-the-planet"         # task10.sh
   ```

   `touch` makes empty files, `mv` removes the original, `cp` keeps it.

6. Task 12: the quest. Follow it by hand in the practice copy:

   ```bash
   cat "$DOJO/CLUE"                          # go to usr/share/doc/quest, read HINT
   cat "$DOJO/usr/share/doc/quest/HINT"      # go to var/cache/quest/old, read NEXT
   cat "$DOJO/var/cache/quest/old/NEXT"      # treasure is in a HIDDEN folder in opt/quest
   ls -a "$DOJO/opt/quest"                   # .hideout  TREASURE (the visible one is a decoy)
   ```

   Then `task12.sh` is:

   ```bash
   cat "$DOJO/opt/quest/.hideout/TREASURE"
   ```

7. Task 13: a folder, then a file in it.

   ```bash
   mkdir "$DOJO/tmp/pwn"
   touch "$DOJO/tmp/pwn/college"
   ```

8. Task 14: find every `flag`.

   ```bash
   find "$DOJO" -name flag
   ```

   Starting `find` from an absolute folder makes it print absolute paths, one per line.

9. Task 15: fool `catflag` with a symbolic link.

   ```bash
   ln -s "$DOJO/flag" ~/not-the-flag
   "$DOJO/challenge/catflag"
   ```

   `catflag` runs `cat "$HOME/not-the-flag"`; the link sends that `cat` on to `$DOJO/flag`. Target comes first in `ln -s`.

10. Run `./check`. Each script runs in a fresh copy, so the order does not matter.

**Check.** `./check` prints `15/15 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- `./try 9` really moves the practice `dojo/flag`, so `./try 10` and `./try 15` then fail by hand. That is only the practice copy; `./check` is unaffected. Restart the challenge to get a fresh practice copy if needed.
- Swapping the order in `ln -s` (link name first). The link then points the wrong way and `catflag` prints nothing.
- Copying the practice treasure text into an `echo` for task 12. The check uses a different secret.
