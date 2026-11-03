## Pondering PATH

*llp-path · easy*

**Goal.** Fill in `answers/task1.sh` to `answers/task6.sh` to read PATH, find which program a name runs, add folders to PATH (for now and for every new shell), and shadow a real command with your own.

**You need to know.**

- PATH is a colon-separated list of folders, searched left to right.
- `command -v NAME` shows what would run; `type -ap NAME` lists every match.
- `export PATH="DIR:$PATH"` puts a folder first for this shell and its children.
- `~/.bashrc` runs at the start of every new interactive bash.

**Walkthrough.**

`./check` runs each script with its own PATH and sets `HOME` to a sandbox folder, so writing to `$HOME` is safe. Remove the `# TODO` line in every file.

1. Task 1, one PATH folder per line.

   ```bash
   #!/bin/bash
   echo "$PATH" | tr ':' '\n'
   ```

   `tr` swaps each colon for a newline, which keeps the folders in order.

2. Task 2, full path of the command in `$1`.

   ```bash
   #!/bin/bash
   command -v "$1"
   ```

   `command -v` is a shell builtin that searches PATH exactly like the shell does.

3. Task 3, run `beacon` from `tools/`.

   ```bash
   #!/bin/bash
   export PATH="$PWD/tools:$PATH"
   beacon
   ```

   `$PWD/tools` is an absolute path, so the entry still works if the folder changes later.

4. Task 4, your own bin folder.

   ```bash
   #!/bin/bash
   mkdir -p "$HOME/bin"
   printf '#!/bin/bash\necho "hello from pi"\n' > "$HOME/bin/hello-pi"
   chmod +x "$HOME/bin/hello-pi"
   echo 'export PATH="$HOME/bin:$PATH"' >> "$HOME/.bashrc"
   export PATH="$HOME/bin:$PATH"
   hello-pi
   ```

   The single quotes put the literal text `$HOME/bin` into `.bashrc` so it expands in each new shell; the second `export` makes it work in this script right now.

5. Task 5, shadow `date`.

   ```bash
   #!/bin/bash
   mkdir -p fake
   printf '#!/bin/bash\necho 1999\n' > fake/date
   chmod +x fake/date
   PATH="$PWD/fake:$PATH" ./report.sh
   ```

   `report.sh` calls `date +%Y`; with `fake/` first in PATH it finds the fake `date` that prints `1999`, and `report.sh` is never edited.

6. Task 6, every `tool` in PATH order.

   ```bash
   #!/bin/bash
   type -ap tool
   ```

   `-a` lists all matches instead of only the first, and `-p` prints them as file paths.

7. Run the checker.

   ```bash
   ./check
   ```

**Check.** `./check` prints `6/6 tasks pass` and then `CHECK_OK`. Then press Done.

**Common mistakes.**

- Writing `export PATH=tools:$PATH` with a relative folder, or putting the new folder at the end in task 5, so the real `date` still wins.
- Using double quotes in the `.bashrc` line, which saves today's expanded PATH instead of `$HOME/bin:$PATH`.
- Using `which` for task 6: it shows only the first match.
