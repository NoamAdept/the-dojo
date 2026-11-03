# Pondering PATH

Are you new to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

Write each answer as a bash script in `answers/taskN.sh`. `./check` runs each script with its own PATH and its own folders.

1. **Read PATH**: print each folder of your PATH on its own line, in order.
2. **Find a command**: `$1` is the name of a command. Print the full path of the program that the shell would run for it.
3. **Use PATH**: the folder `tools/` holds a program called `beacon`. Add `tools/` to your PATH. Then run it by typing only `beacon`.
4. **Your own bin**: do 3 things.
   - Create `$HOME/bin/hello-pi`. It must be executable and print `hello from pi`.
   - Add `$HOME/bin` to PATH in `$HOME/.bashrc`, so that it works in every new shell.
   - Run `hello-pi` once.
5. **Shadow a command**: `report.sh` uses `date`. Run `report.sh` so that it reports the year `1999`. Do not edit `report.sh`. Instead, put your own `date` in a folder at the front of PATH.
6. **Every match**: several folders in PATH have a program called `tool`. Print the full path of each one, in PATH order. The one that runs first comes first.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
