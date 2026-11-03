# Environment: lesson

Every process carries a small list of named text values. These values are
called environment variables. Programs read them to get settings. For
example, a variable can say where your home folder is, or which language
to use. The names are usually in CAPITAL letters:

```
$ printenv HOME
/home/student
$ echo "$HOME"
/home/student
```

If you give printenv no name, it prints all the variables. It prints one
NAME=value per line. That list is long. So filter it with grep. In a grep
pattern, ^ means "at the start of the line":

```
$ printenv | grep '^LANG'
LANG=en_GB.UTF-8
```

You can make your own variable with export. Every program you start from
that shell then inherits it. "Inherits" means it gets a copy:

```
$ export COLOR=blue
$ printenv COLOR
blue
```

Important: a variable lives inside a process, not in a file. Suppose a
script sets some variables and then starts a new shell. Only that new
shell has the variables. This is why you cannot see the real values by
reading lab_shell.sh. You must go inside the lab shell and ask it.

A shell inside a shell: `./lab_shell.sh` starts a new bash shell for you.
Your prompt may look the same as before. Type exit to leave it. Then you
are back in your normal shell. The variables go away with the lab shell.

Joining text: "$A$B" gives the value of A, and then directly the value of
B. ${A}${B} means the same thing. The curly braces only make the names
clear. printf '%s\n' prints that text and then a newline:

```
$ export X=sun Y=flower
$ printf '%s\n' "${X}${Y}"
sunflower
```

The order matters. "${Y}${X}" would print flowersun.

## New words
- **environment variable**: a named text value that a process carries.
- **printenv**: prints environment variables.
- **export**: makes a shell variable an environment variable.
- **inherit**: a new process gets a copy of its parent's environment.
- **^ (in grep)**: matches the start of a line.
- **exit**: leaves the current shell.

## Offline help

- man printenv
- man 7 environ   (offline: what the environment is)
