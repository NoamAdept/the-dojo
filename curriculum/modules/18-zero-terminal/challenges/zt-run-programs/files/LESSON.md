# Running Programs and Reading Errors: lesson

### Running a program in this folder

Commands like `ls` and `date` live in special system folders. When you type a bare name (a name
with no path), the shell looks only in those folders. So it does not find a program that is in
**your** folder:

```console
$ greet
bash: greet: command not found
```

To run it, give its path. `.` means "this folder". So `./greet` means "the program `greet`,
right here":

```console
$ ./greet
Hello! ...
```

This is why you type `./check`. It runs the `check` program in this folder.

### The three errors you will meet most

An error message usually has this form: `who: what: problem`. Read it slowly. Start from the end.

- **`command not found`**: the shell has no command with that name.
  - Check the spelling and the capital letters.
  - If the program is in this folder, put `./` in front of the name.
- **`Permission denied`**: the file exists, but you are not allowed to do that with it.
  Very often, the file is not marked as a program yet. We say it is "not executable".
  Mark it with `chmod +x NAME`. This means "change mode: add execute". Then run it again.
- **`No such file or directory`**: the name or path you gave does not exist.
  - Check the spelling.
  - Check where you are with `pwd`.
  - Look around with `ls`.

```console
$ ./locked
bash: ./locked: Permission denied
$ chmod +x locked
$ ./locked
unlocked: ...
$ cat nofile.txt
cat: nofile.txt: No such file or directory
```

`ls -l` shows the permissions. Permissions say what you may do with a file.

- A program you can run has an `x` in the first column, like `-rwxr-xr-x`.
- A plain file looks like `-rw-r--r--`.

### Reading ./check

`./check` runs a test for every task. Then it prints a summary like this:

```console
$ ./check
2/4 tasks pass
Not yet:
  - 3 report.txt: AssertionError: there is no file named report.txt in this folder yet
  - 4 config.txt: AssertionError: ./checkme still finds a problem: ...
```

Each line under `Not yet:` starts with a task number. Then it says the problem.

- `AssertionError` just means "a test found something wrong". The words after it say what is wrong.
- `not implemented yet` means you have not started that task.

Fix 1 thing. Run `./check` again. Repeat. When everything passes, it prints `CHECK_OK`.

**Tip:** press the **up arrow** to bring back the last command. Then you do not need to type
`./check` again every time. A later challenge tells you more about this.

### New words

- **`./name`**: run the program `name` that is in the current folder.
- **executable**: a file that is marked as a program. You may run it.
- **permission**: what you are allowed to do with a file (read, write, execute).
- **`chmod +x`**: mark a file as executable.
- **error message**: text that a program prints when something went wrong. It tells you what went wrong.

## Offline help

- Offline: `man chmod`, and `chmod --help`.
