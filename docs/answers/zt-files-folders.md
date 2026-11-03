## Files and Folders

*zt-files-folders · easy*

**Goal.** Create the folders `radio` and `radio/notes`, save `pwd` and `ls` output into files, and find the `key-...` file hidden three folders deep in `maze`, writing its name into `key.txt`.

**You need to know.**

- `pwd` shows the current folder, `ls` lists one, `cd` moves, `mkdir` makes a folder (README, "Looking around and moving" and "Making folders").
- Absolute paths start with `/`, relative paths start from where you stand (README, "Paths").
- `..` is the parent folder; `cd ../..` goes up two levels.
- `>` saves output into a file (from the previous challenge).

**Walkthrough.**

Start in the challenge folder.

1. Tasks 1 and 2: make the folders.

   ```bash
   mkdir radio
   mkdir radio/notes
   ```

   The second `mkdir` uses a relative path, so `notes` is created inside `radio`. `radio` must exist first.

2. Task 3: save `pwd` from inside `radio/notes`.

   ```bash
   cd radio/notes
   pwd > here.txt
   cd ../..
   ```

   `pwd` prints the absolute path of where you stand (ending in `/radio/notes`), and because you are inside that folder, `here.txt` is created there too. `cd ../..` climbs back up two levels to the challenge folder.

3. Task 4: save the maze listing.

   ```bash
   ls maze > maze-list.txt
   ```

   When `ls` writes into a file it puts one name per line: `east`, `north`, `south`, `west`.

4. Task 5: explore the maze.

   ```bash
   cd maze
   ls                # east  north  south  west
   cd north
   ls                # door-1  door-2  door-3
   cd door-3
   ls                # blue  red
   cd blue
   ls                # key-dxjakp
   cd ../../../..
   ```

   Every other branch only holds `dead-end.txt`, so the learner backs out with `cd ..` and tries the next one. Four `..` steps lead from `maze/north/door-3/blue` back to the challenge folder.

5. Write the key name.

   ```bash
   echo key-dxjakp > key.txt
   ./check
   ```

   The answer is `key-dxjakp` (it is in the starter files, so it is the same for every learner). The name must match exactly.

**Check.** `./check` prints `5/5 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Running `pwd > here.txt` in the challenge folder. The file lands in the wrong place, and the check says so. Fix: `cd radio/notes` first.
- Running `ls maze > maze-list.txt` from inside `maze` (it then fails, because there is no `maze` in there). Go back to the challenge folder first.
- Losing track of where they are. Tell them to run `pwd` whenever in doubt.
