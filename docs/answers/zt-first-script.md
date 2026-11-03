## Your First Scripts

*zt-first-script · easy*

**Goal.** Fill in four small bash scripts in `answers/`: print one line, print three lines, create a file, and create a folder with a file inside it.

**You need to know.**

- A script is a text file of commands, run from top to bottom (README lesson on scripts).
- `#!/bin/bash` names the interpreter; `#` starts a comment.
- `./try N` runs `answers/taskN.sh` in a fresh, empty `practice/` folder, just like `./check` does.
- Editing with vim: `vim FILE`, `dd` deletes the TODO line, `O` opens a new line above the cursor to type in, `Esc` then `:wq` Enter saves and quits.

**Walkthrough.**

Each answer file starts with `#!/bin/bash` and a TODO comment. Keep the first line and replace the TODO line.

1. Task 1: print a line. In `answers/task1.sh`:

   ```bash
   #!/bin/bash
   echo hello from my script
   ```

   Test it:

   ```bash
   vim answers/task1.sh
   ./try 1
   ```

   The script holds exactly what you would type at the prompt, without the `$`.

2. Task 2: three lines. In `answers/task2.sh`:

   ```bash
   #!/bin/bash
   echo ready
   echo steady
   echo go
   ```

   Each `echo` prints its own line, and the commands run in order.

3. Task 3: make a file. In `answers/task3.sh`:

   ```bash
   #!/bin/bash
   echo made by a script > result.txt
   ```

   A relative file name is created in the folder where the script runs. That is why the checker and `./try` find it in their fresh folder.

   ```bash
   ./try 3
   cat practice/result.txt
   ```

4. Task 4: a folder and a file. In `answers/task4.sh`:

   ```bash
   #!/bin/bash
   mkdir box
   echo inside > box/note.txt
   ```

   The folder must exist before `>` can write a file into it, so `mkdir` comes first.

   ```bash
   ./try 4
   ls practice/box
   ```

5. Run `./check`.

**Check.** `./check` prints `4/4 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Making `result.txt` by hand at the prompt instead of in the script. The checker runs each script in an empty folder, so the script must create the file itself.
- Putting all three words of task 2 into one `echo`. That prints one line, not three.
- Leaving the TODO line and typing the command on the same line after `#`. Everything after `#` is a comment, so nothing runs.
