## Find the Flag

*orient-find-flag · easy*

**Goal.** Explore the `labyrinth/` folder, skip the decoys, and read the one real flag (text shaped like `flag{...}`). Then submit it.

**You need to know.**

- `pwd`, `ls`, `ls -la`, `cd`, `cat` (README, "Lesson").
- Hidden files and folders start with a dot and only show with `ls -a`.
- `find . -type f` lists every file in the tree, hidden ones included.

**Walkthrough.**

1. Look around the challenge folder.

   ```bash
   pwd
   ls -la
   cat NOTES.txt
   ```

   `ls -la` shows hidden entries too, and `NOTES.txt` hints that the flag is "deeper than the first turn" of the labyrinth.

2. List every file in the maze at once.

   ```bash
   find . -type f
   ```

   `find` walks all folders, including hidden ones. Among the results are `labyrinth/west/deadend/readme.txt`, `labyrinth/north/alcove/flag.txt`, `labyrinth/east/hint.txt` and two files inside the hidden folder `labyrinth/east/tunnel/.cache/`.

3. Open the candidates and reject the decoys.

   ```bash
   cat labyrinth/north/alcove/flag.txt
   cat labyrinth/east/hint.txt
   cat labyrinth/east/tunnel/.cache/notes.bak
   ```

   `flag.txt` and `notes.bak` contain text starting with `decoy{`, not `flag{`, and `hint.txt` says to keep going east into the tunnel.

4. Read the real flag.

   ```bash
   cat labyrinth/east/tunnel/.cache/secret.flag
   ```

   This is the only file whose content starts with `flag{`. It sits in a hidden `.cache` folder, which is why plain `ls` never shows it.

   A quicker way an instructor can show afterwards:

   ```bash
   grep -r 'flag{' labyrinth
   ```

5. Submit. Either paste the flag in the dojo, or:

   ```bash
   academy submit 'flag{...}'
   ```

   Replace `flag{...}` with the text printed by step 4, and keep the single quotes so zsh does not treat the braces as special.

**Check.** The dojo (or `academy submit`) accepts the flag printed by `cat labyrinth/east/tunnel/.cache/secret.flag`.

**Common mistakes.**

- Submitting the content of `labyrinth/north/alcove/flag.txt` because of its file name. It is a decoy; check that the text starts with `flag{`.
- Using `ls` without `-a` and never seeing the `.cache` folder.
- Submitting the flag without quotes in zsh, where `{...}` can be mangled.
