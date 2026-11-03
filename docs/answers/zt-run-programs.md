## Running Programs and Reading Errors

*zt-run-programs · easy*

**Goal.** Run four small programs in the challenge folder, fix the three classic errors (`command not found`, `Permission denied`, `No such file or directory`), and save each program's output into a file. Then fix `config.txt` until `./checkme` prints `ALL GOOD`.

**You need to know.**

- A program in the current folder is run as `./name`; a bare name is only searched in the system folders (README lesson on running programs).
- `chmod +x FILE` makes a file executable.
- How to read an error from the end: the last part names the problem.
- `mkdir`, `vim` and `>` from the earlier challenges.

**Walkthrough.**

1. Task 1: see the error, then run `greet` properly.

   ```bash
   greet                 # bash: greet: command not found
   ./greet > greet.txt
   cat greet.txt         # Hello! Your code is 42-beacon
   ```

   Without `./` the shell looks only in the system command folders and gives up. `./greet` means "the file `greet` in this folder".

2. Task 2: fix `Permission denied`.

   ```bash
   ./locked              # Permission denied
   chmod +x locked
   ./locked > locked.txt # unlocked: 5150-door
   ```

   `locked` is a script without the execute permission. `chmod +x` adds it, so the shell is now allowed to run it.

3. Task 3: create the missing file for `report`.

   ```bash
   ./report              # cat: data/settings.txt: No such file or directory
   mkdir data
   vim data/settings.txt
   ```

   In vim press `i`, type `volume=7`, then press `Esc` and type `:wq` Enter. Then:

   ```bash
   ./report              # report ready, settings: volume=7
   ./report > report.txt
   ```

   The error names the exact path the program wanted, so creating `data/settings.txt` makes it work.

4. Task 4: follow `./checkme` one problem at a time.

   ```bash
   ./checkme
   vim config.txt
   ```

   The starting file is `name = my radio`, `band=FM`, `gain=ten`. `./checkme` complains in this order: spaces around `=`, then the name must be `pi-radio`, then `fm` must be lower case, then `gain` must be digits. Run `./checkme` after every fix (the up arrow repeats it). The finished file:

   ```text
   name=pi-radio
   band=fm
   gain=10
   ```

   Any number works for `gain`, as long as it is written with digits.

5. Run `./check`.

**Check.** `./checkme` prints `ALL GOOD: config.txt is correct.` and `./check` prints `4/4 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Writing `chmod +x ./locked > locked.txt`, which saves nothing useful. `chmod` and running the program are two separate commands.
- Saving `report.txt` before `data/settings.txt` exists. The file then holds nothing (the error goes to the screen). Run `./report > report.txt` again once it works.
- Typing `Volume=7` or `band=FM`. Linux treats upper and lower case as different.
