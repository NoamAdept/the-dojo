## File Globbing

*lls-globbing · easy*

**Goal.** Write ten scripts that use the glob characters `*`, `?`, `[]` and `[!]` to hand programs the right file names, and use `compgen` to print what Tab completion would offer.

**You need to know.**

- The shell expands `*` (any text), `?` (one character) and `[abc]` (one of these) before the program starts (README lesson).
- `[!abc]` matches one character that is NOT in the list.
- Globs stay literal inside quotes, so keep the glob part outside: `"$DOJO"/challenge/files/file_[absh]`.
- `compgen -f PREFIX` lists file completions, `compgen -c PREFIX` lists command completions.
- Test a glob with `echo` first: `echo *p*` shows exactly what a program would get.

**Walkthrough.**

Run `. ./env.sh` to try things by hand. Every answer file starts with `#!/bin/bash`.

1. Task 1: `*` in a `cd`.

   ```bash
   cd "$DOJO"/ch*
   "$DOJO/challenge/run"
   ```

   `ch*` is 3 characters and matches only `challenge` (plain `c*` would also match `cache`).

2. Task 2: `?` for every `c` and `l`.

   ```bash
   cd "$DOJO"/?ha??enge
   "$DOJO/challenge/run"
   ```

   Each `?` stands for exactly one character: `c`, `l`, `l`.

3. Task 3: one `[]` glob for four files.

   ```bash
   cd "$DOJO/challenge/files"
   "$DOJO/challenge/run" file_[absh]
   ```

   `[absh]` matches one character out of a, b, s, h, so the shell passes four names.

4. Task 4: the same, as absolute paths, without `cd`.

   ```bash
   "$DOJO/challenge/run" "$DOJO"/challenge/files/file_[absh]
   ```

   The variable is quoted, the glob is not, so it still expands into four full paths.

5. Task 5: two stars, at most 3 characters.

   ```bash
   cd "$DOJO/challenge/words"
   "$DOJO/challenge/run" *p*
   ```

   `*p*` means "anything, a p, anything", so every word with a `p` matches.

6. Task 6: only `challenging`, `educational` and `pwning`.

   ```bash
   cd "$DOJO/challenge/words"
   "$DOJO/challenge/run" [cep]*
   ```

   These three are the only words starting with c, e or p.

7. Task 7: everything NOT starting with p, w or n.

   ```bash
   cd "$DOJO/challenge/words"
   "$DOJO/challenge/run" [!pwn]*
   ```

8. Task 8: file completions.

   ```bash
   compgen -f "$DOJO/challenge/pwnc"
   ```

   `compgen -f` prints what Tab would complete. The check renames the file, so a fixed name fails.

9. Task 9: several completions.

   ```bash
   compgen -f "$DOJO/challenge/tabfiles/pwncollege-f"
   ```

   It prints one match per line (`family`, `flamingo`, `flyswatter` in the practice copy).

10. Task 10: command completions, each once.

    ```bash
    compgen -c pwncollege | sort -u
    ```

    `compgen -c` searches every `PATH` folder and can list a name twice; `sort -u` removes repeats.

11. Test with `./try N`, then `./check`.

**Check.** `./check` prints `10/10 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Putting the glob inside the quotes, like `"$DOJO/challenge/files/file_[absh]"`. The program then gets that text literally.
- Typing `c*` in task 1. It matches `cache` and `challenge`, so `cd` gets two arguments and fails.
- Writing out file names for tasks 8 to 10. The check renames files each run, so only `compgen` works.
