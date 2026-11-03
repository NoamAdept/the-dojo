# Pondering Paths

Linux keeps every file in 1 tree of folders. The tree starts at the **root**, `/`.
A path that starts with `/` is an **absolute path**, like `/challenge/run`.
It names the same file, in any folder you are in.
You can run a program just by typing its path.

Every process (running program) has a **current working directory** (the folder it is in now).
`cd DIR` changes it, and `pwd` prints it.
A path that does not start with `/` is a **relative path**.
The shell looks for it starting from the working directory:

| working directory | path to `/tmp/a/b/my_file` |
|---|---|
| `/` | `tmp/a/b/my_file` |
| `/tmp` | `a/b/my_file` |
| `/tmp/a/b/c` | `../my_file` |

Every directory has 2 special entries: `.` (the directory itself) and `..` (its parent, the directory 1 level up).
So `./challenge/run` and `challenge/./run` mean the same as `challenge/run`.

There is 1 safety rule.
Bash never looks for a plain word like `run` in the current directory.
It only searches the folders in `$PATH`.
So to run a program in the current directory, you type `./run`.

**Home.** Your home directory is the folder where your own files are.
When a word starts with `~`, bash replaces the `~` with the path of your home directory.
So `echo ~/notes` prints something like `/home/hacker/notes`.
Bash only does this for a `~` at the start of a word.
`cd` with no argument takes you to your home directory.

In these tasks, `$DOJO` takes the place of `/`.
So the program `/pwn` from the original level is `"$DOJO/pwn"` here.
Every program below only reports how and where it was started.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

1. **The root**: run `$DOJO/pwn` using its absolute path (`"$DOJO/pwn"`).
2. **Program and absolute paths**: run `$DOJO/challenge/run` using its absolute path.
3. **Position thy self**: run `$DOJO/challenge/position`. Your working directory must be `$DOJO/var/lib/academy` when you run it.
4. **Position elsewhere**: run `$DOJO/challenge/tour` 5 times. Run it from these working directories, in this order: `$DOJO/etc`, `$DOJO/usr/share`, `$DOJO/var/log`, `$DOJO/home`, `$DOJO/tmp`.
5. **Implicit relative path**: `cd` to `$DOJO`. Then run the program with the relative path `challenge/run` (with no `/` or `.` at the start).
6. **Explicit relative path**: `cd` to `$DOJO`. Then run `challenge/run` with a relative path that contains a `.` directory, such as `./challenge/run`.
7. **Implicit relative path, in place**: `cd` to `$DOJO/challenge`. Then run `run` from there as `./run`.
8. **Home sweet home**: `$DOJO/challenge/copyflag PATH` writes a secret to PATH. It only does this if PATH is absolute and inside your home directory. Run it with an argument that starts with `~/` and that you type with 3 characters or fewer. (Bash expands it to an absolute path.)

## Check your work

You can run `./check` as many times as you want. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
