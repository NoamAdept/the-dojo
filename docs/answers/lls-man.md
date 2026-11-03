## Digesting Documentation

*lls-man · easy*

**Goal.** Use man pages, `--help` and the `help` builtin to find the right options for two practice programs, and search a folder of man pages with `grep`. Seven one-line scripts.

**You need to know.**

- Opening a page file with `man -l FILE` and searching inside it with `/word`, `n`, `q` (README, "Man pages").
- `grep -n WORD FILE` searches a page file without opening man; `grep -rl` lists matching files in a folder.
- `PROGRAM --help` for programs without a man page.
- `help NAME` documents shell builtins like `pwd`.

**Walkthrough.**

Run `. ./env.sh` first. Every answer file starts with `#!/bin/bash`.

1. Task 1: the documented option.

   ```bash
   "$DOJO/challenge/challenge" --giveflag
   ```

2. Task 2: an option that takes its own argument.

   ```bash
   "$DOJO/challenge/challenge" --printfile "$DOJO/flag"
   ```

   `"$DOJO/flag"` is the argument that belongs to `--printfile`.

3. Task 3: read the manual.

   ```bash
   man -l "$DOJO/usr/share/man/man1/challenge.1"
   ```

   The DESCRIPTION lists `--sesame`: "print the manual success message". So `task3.sh` is:

   ```bash
   "$DOJO/challenge/challenge" --sesame
   ```

4. Task 4: search a long manual. Open `challenge-full.1` with `man -l`, type `/search success` and press Enter, then `n` until the line that does not say "does not". Or outside man:

   ```bash
   grep -n -B1 "print the search success" "$DOJO/usr/share/man/man1/challenge-full.1"
   ```

   The match is `--aurora-borealis`, so `task4.sh` is:

   ```bash
   "$DOJO/challenge/challenge" --aurora-borealis
   ```

5. Task 5: which pages mention `challenge`.

   ```bash
   grep -rl challenge "$DOJO/usr/local/man/man1"
   ```

   `-r` searches every file in the folder and `-l` prints only the file names. The check fills the folder with new random pages, so the script must search, not list fixed names.

6. Task 6: a program with only `--help`.

   ```bash
   "$DOJO/challenge/helpful" --help
   ```

   The help lists `--open-the-pod-bay-doors    print the success message`. So `task6.sh` is:

   ```bash
   "$DOJO/challenge/helpful" --open-the-pod-bay-doors
   ```

7. Task 7: docs for a builtin.

   ```bash
   help pwd
   ```

   `pwd` lives inside bash, so `help` (not `man`) documents it. The check compares the output byte for byte with `help pwd`.

8. Test with `./try N`, then `./check`.

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Using the first "success" match in `challenge-full`. Dozens of options say "does not print any success message"; only one says "print the search success message".
- Hard-coding the page name found in the practice copy for task 5. It changes every check run.
- Writing `man pwd` or `pwd --help` for task 7. The output must match `help pwd` exactly.
