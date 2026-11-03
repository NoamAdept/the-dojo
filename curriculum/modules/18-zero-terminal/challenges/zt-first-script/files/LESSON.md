# Your First Scripts: lesson

### What is a script?

A **script** is a text file full of commands. When you run the script, bash runs those
commands. It runs them one line after the other, from top to bottom. This is the same as if
you typed them yourself. The name of a bash script usually ends in `.sh`.

Look at one of the answer files:

```console
$ cat answers/task1.sh
#!/bin/bash
# TODO: replace this line with your command(s) for task 1.
```

- Line 1 is `#!/bin/bash`. It tells the computer "run this file with bash". Do not change it.
- A line that starts with `#` is a **comment**. A comment is a note for people. Bash skips it.
- The `TODO` line is a placeholder. A placeholder only keeps the place for your work.
  **Delete it** and write your command there instead. While the word `TODO` is still in the
  file, `./check` reports the task as `not implemented yet`.

### Writing an answer

Open the file with vim. Replace the TODO line. Then save and quit:

```console
$ vim answers/task1.sh
```

After you edit it, the file might look like this:

```bash
#!/bin/bash
echo hello from my script
```

### Testing it

You can run a script with `bash` and its path:

```console
$ bash answers/task1.sh
hello from my script
```

`./try N` also runs the script for task N. But it runs it the same way the checker does.
The next section explains this.

```console
$ ./try 1
hello from my script
```

Then `./check` runs all your scripts. It tells you what passes.

### Where does the script run?

The checker does not run your script in this challenge folder. It runs each script in a new,
empty folder. It deletes that folder afterwards.

So if a script does `echo done > result.txt`, it creates `result.txt` in **that** folder.
The checker looks for the file there.

`./try N` copies this behavior with a folder called `practice/`. After `./try 3`, look inside
with `ls practice`. Note: `./try` empties `practice/` every time it starts.

This means: **write commands that do the job. Do not do the job by hand.** If you make the
file yourself in the terminal, it does not help. The script must make it.

### New words

- **script**: a text file of commands that run one after another.
- **`#!/bin/bash`**: the first line of a bash script. It says which program runs the file.
- **comment**: a line that starts with `#`. Bash ignores it.
- **TODO**: a placeholder. It means "there is still something to do here".
- **`./try N`**: run your task N script the same way `./check` does.

## Offline help

- Offline: `help echo` (echo is built into bash) and `man bash` (long; press `q` to leave).
