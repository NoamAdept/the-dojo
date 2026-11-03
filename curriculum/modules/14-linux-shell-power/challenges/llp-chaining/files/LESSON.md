# Chaining Commands and Scripts: lesson

**Chaining.** You can put several commands on one line. The sign between them decides
what happens:

```bash
mkdir out ; cd out     # ; runs the second no matter what
make && ./app          # && runs the second only if the first succeeded (exit code 0)
ping -c1 pi || echo "pi is offline"   # || runs the second only if the first failed
```

- `;` always runs the second command.
- `&&` runs the second command only if the first one succeeded. Success means exit code 0.
  (The exit code is the number a command gives back when it ends.)
- `||` runs the second command only if the first one failed.

**Scripts.** A shell script is a file with these commands in it. `bash myscript.sh` runs
it. You can also run it as `./myscript.sh`. For that, it needs 2 things:

1. a **shebang** as the first line: `#!/bin/bash`. It tells the kernel (the core of the
   operating system) which interpreter (the program that reads and runs the script) to use;
2. the **execute bit** (the permission to run the file): `chmod +x myscript.sh`.

**Arguments.** Arguments are the words you type after the script name. Inside a script:

- `$1`, `$2`, ... are the arguments.
- `$#` is the number of arguments.
- `$@` is all of them.

Put them in double quotes (`"$1"`). Then an argument that has spaces stays as 1 word.

```bash
#!/bin/bash
echo "Hello, $1! You gave me $# arguments."
```

**Decisions.** `if` runs a command and checks its exit code. The usual condition is
`[ ... ]`. This is the `test` command:

```bash
if [ -f "$1" ]; then
    echo "file exists"
elif [ -d "$1" ]; then
    echo "it is a directory"
else
    echo "nothing there"
    exit 1            # a script can choose its own exit code
fi
```

Useful tests:

- `-f FILE`: true if FILE is a regular file.
- `-d DIR`: true if DIR is a directory (folder).
- `-e PATH`: true if anything exists at PATH.
- `"$a" = "$b"`: compares 2 strings (text).
- `-lt -le -eq -ne -ge -gt`: compare numbers. They mean less than, less or equal, equal,
  not equal, greater or equal, greater than. Example: `[ "$n" -lt 0 ]`.

The spaces inside the brackets are important. Do not leave them out.

`./check` puts small helper programs in the folder for each task. Sometimes they succeed
and sometimes they fail. So your chaining must really react to the exit codes.

### New words

- **exit code**: the number a command gives back when it ends. 0 means success.
- **script**: a file of commands that runs from top to bottom.
- **shebang**: the first line `#!/bin/bash`. It names the interpreter for the script.
- **interpreter**: the program that reads a script and runs it, for example bash.
- **execute bit**: the permission that lets you run a file as a program.
- **argument**: a word that you give to a command or script after its name.
