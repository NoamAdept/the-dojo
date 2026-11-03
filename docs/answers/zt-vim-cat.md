## Creating and Editing Text Files

*zt-vim-cat · easy*

**Goal.** Use vim to create `shopping.txt`, fix a typo in `poem.txt` and write `code.txt`, then use `cat` to join two files into `both.txt`.

**You need to know.**

- `vim FILE` opens or creates a file (LESSON, "The vim editor").
- vim starts in Normal mode, where keys are commands. Press `i` for Insert mode (the bottom line shows `-- INSERT --`) and type; press `Esc` to go back to Normal mode.
- In Normal mode: `:wq` Enter saves and quits, `:q!` Enter quits without saving. `x` deletes the character under the cursor, `a` starts typing just after the cursor, `dd` deletes a line, `u` undoes.
- `cat A B` prints files one after the other; add `> FILE` to save that (LESSON, "Reading a file with cat").

**Walkthrough.**

1. Task 1: create the shopping list.

   ```bash
   vim shopping.txt
   ```

   Press `i`, then type these three lines, pressing Enter after each:

   ```text
   antenna
   cable
   battery
   ```

   Press `Esc`, type `:wq` and press Enter. Check with `cat shopping.txt`. Each word must be on its own line, in this order.

2. Task 2: fix the typo.

   ```bash
   vim poem.txt
   ```

   Stay in Normal mode. Move with the arrow keys down to line 2, `The radoi hums softly`. Put the cursor on the `o` in `radoi` and press `x` (the line now reads `radi`). Then press `a` to start typing after the `i`, type `o`, and press `Esc`. Type `:wq` and Enter. The finished line reads `The radio hums softly`. Nothing else in the file may change.

   Another way: put the cursor on the `r` of `radoi`, type `cw`, type `radio`, press `Esc`, then `:wq` Enter.

3. Task 3: read the message.

   ```bash
   cat message.txt
   ```

   The message gives the code word `violet-6666` and asks for a file `code.txt` holding it, made with vim.

   ```bash
   vim code.txt
   ```

   Press `i`, type `violet-6666`, press `Esc`, then `:wq` Enter.

4. Task 4: join the two files.

   ```bash
   cat shopping.txt poem.txt > both.txt
   ./check
   ```

   `cat` prints `shopping.txt` and then `poem.txt`, and `>` saves that combined text into `both.txt`.

**Check.** `./check` prints `4/4 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Typing words in Normal mode. The keys run as commands (for example `x` deletes, `d` waits for more), so the text gets mangled. Press `Esc`, then `u` a few times to undo, then press `i` before typing.
- Typing `:wq` while still in Insert mode. It lands in the file as text instead of saving. Press `Esc` first, then `:wq` Enter, and delete the stray `:wq` with `x` if it got in.
- Typing `:q` and seeing `E37: No write since last change`. vim refuses to quit with unsaved work. Use `:wq` to keep the changes or `:q!` to throw them away.
- Getting lost (odd text at the bottom, keys doing strange things). Press `Esc` twice, type `:q!` and Enter. The file is unchanged and you can start again.
- Pressing `x` in the wrong place in `poem.txt`. Press `u` to undo it before saving.
- Making `both.txt` first and fixing `poem.txt` later. The check compares against the current files, so run the `cat ... > both.txt` command again after any edit.
