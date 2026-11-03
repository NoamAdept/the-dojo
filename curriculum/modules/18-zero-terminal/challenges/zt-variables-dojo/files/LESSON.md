# Variables, Quotes and the Practice Dojo: lesson

### Variables

A **variable** is a name that holds a piece of text. To read a variable, put `$` in front of
its name. The shell replaces `$NAME` with the value. Then it runs the command.

Some variables already exist. For example, `HOME` holds the path of your home folder:

```console
$ echo $HOME
/home/hacker
$ echo my home is $HOME
my home is /home/hacker
```

A `~` at the start of a path is a short way to write your home folder. So `~/notes` means
`$HOME/notes`.

You can make your own variable with `NAME=value`. **Do not put spaces around the `=`.**
With spaces, the shell thinks `NAME` is a command.

```console
$ band=fm
$ echo listening on $band
listening on fm
```

### Double quotes

The shell splits lines at spaces. This is a problem when a file or folder name has a space in
it, like `my notes`:

```console
$ cat my notes/today.txt
cat: my: No such file or directory
cat: notes/today.txt: No such file or directory
$ cat "my notes/today.txt"
Practice notes: ...
```

**Double quotes** `"..."` fix this:

- Text inside double quotes stays together as 1 argument.
- The shell still replaces `$variables` inside double quotes.

So here is a safe habit: always write variables inside double quotes, like `"$HOME/notes"`.

### $DOJO and the practice copy

The shell challenges give you a small fake filesystem to explore. A filesystem is the tree of
folders and files on a computer. With a fake one, you can practise without touching your real
files.

The variable `DOJO` holds the top folder of this fake filesystem. During `./check`:

- `$DOJO` points at a new copy with **different secrets**.
- `$HOME` is `$DOJO/home/hacker`.

So your script must use paths like `"$DOJO/message.txt"`. Never use a path that you copied from
your screen.

In this folder, `dojo/` is the practice copy. To set `DOJO` in your own terminal, run:

```console
$ . ./env.sh
DOJO is now /home/hacker/challenge/dojo
$ ls "$DOJO"
home  message.txt  my notes  tmp
```

The first `.` means "run this file inside my current shell". So the variable that the file
sets is still there afterwards. Did you open a new terminal? Then run it again.

`./try N` sets `DOJO` and `HOME` by itself. Then it runs your task N script from `$HOME`. This
is the same as `./check`.

### New words

- **variable**: a name that holds text. You read it with `$NAME`.
- **`$HOME` and `~`**: your home folder.
- **double quotes**: keep text with spaces together as 1 argument. `$variables` still work inside.
- **`$DOJO`**: the top folder of the challenge's fake filesystem.
- **`. ./env.sh`**: run env.sh in your current shell, so `DOJO` stays set.
