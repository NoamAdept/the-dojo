# Pondering PATH: lesson

When you type `ls`, how does the shell find the program? It uses the **PATH** variable.
PATH is a list of folders. The shell looks in each folder, in order. It runs the first
executable file (a file that you are allowed to run) named `ls`.

```bash
echo "$PATH"
# /home/pi/bin:/usr/local/bin:/usr/bin:/bin
```

A colon (`:`) separates the folders. Some commands have a `/` in them, like `./tool` or
`/usr/bin/ls`. The shell does not search PATH for these commands at all. The shell also
skips files that do not have the execute bit (the permission to run the file).

**Where is that command?**

```bash
command -v python3   # /usr/bin/python3 (a bash builtin, works everywhere)
which python3        # the same for programs
type -a python3      # every match, in PATH order
which -a python3     # every match, in PATH order
```

- `command -v` is a bash builtin (a command that is part of bash itself). It works everywhere.
- `which` does the same for programs.
- `type -a` and `which -a` show every match, in PATH order.

**Changing PATH.** You can add a folder to PATH in 2 ways:

- Put it at the front (prepend). Then its programs win.
- Put it at the end (append). Then its programs are only used if nothing else matches.

`export` makes the change visible to programs that you start from this shell:

```bash
export PATH="$HOME/bin:$PATH"     # for this shell and its children only
```

This change only lasts for this shell. To make it permanent, add that line to `~/.bashrc`.
Bash reads this file every time it starts.

**Shadowing.** The first match wins. So a folder early in PATH can replace a system
command. We call this *shadowing*. It is useful for testing. For example, a fake `date`
can always print the same day.

It can also be dangerous. Think of a script that runs with special rights (a privileged
script). If a folder early in its PATH can be changed by other people, someone can put a
fake program there. Then the script runs that program instead. This is called hijacking.
This is why scripts that run as root (the admin user) often set PATH themselves. Or they
use full paths to every program.

### New words

- **PATH**: a variable that lists the folders where the shell looks for programs.
- **executable**: a file that you are allowed to run as a program.
- **builtin**: a command that is part of the shell itself, not a separate program.
- **prepend / append**: add to the front / add to the end.
- **shadowing**: a program early in PATH hides a program with the same name later in PATH.
- **root**: the admin user, who can do anything on the system.
