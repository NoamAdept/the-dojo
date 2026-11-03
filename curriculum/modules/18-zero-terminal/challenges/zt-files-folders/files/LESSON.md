# Files and Folders: lesson

### Files and folders

A **file** holds data, like text or a picture. A **folder** holds files and other folders.
Linux people also say **directory** for a folder. Folders inside folders make a tree.

The shell is always "standing" inside one folder. We call it the **current folder**.
Another name for it is the working directory. When the dojo opens your terminal, you stand
in this challenge's folder.

`pwd` tells you where you are. The name means "print working directory".

```console
$ pwd
/home/hacker/challenge
```

### Paths

That answer is a **path**. A path is the list of folders you walk through. A `/` separates
each folder name.

`/home/hacker/challenge` means:

1. Start at the very top. This is the first `/`. We call it the **root**.
2. Go into `home`.
3. Then go into `hacker`.
4. Then go into `challenge`.

A path that starts with `/` is an **absolute path**. It works from any folder.

A path that does not start with `/` is a **relative path**. It starts from the current folder.
`maze/north` means "the folder `north`, inside the folder `maze`, which is right here".

There are 2 special names:

- `..` means "the folder above this one". We call it the parent folder.
- `.` means "this folder".

### Looking around and moving

`ls` lists what is in the current folder. `ls maze` lists what is in `maze`:

```console
$ ls
README.md  check  check.py  maze
$ ls maze
east  north  south  west
```

`cd` moves you into another folder. The name means "change directory". It prints nothing.
Use `pwd` to see where you are now:

```console
$ cd maze
$ pwd
/home/hacker/challenge/maze
$ cd ..
$ pwd
/home/hacker/challenge
```

The prompt usually shows the current folder too. Did you get lost? Then use these:

- `cd ..` goes up 1 level.
- `cd ../..` goes up 2 levels.

If you type `cd` alone, it takes you to your **home folder**. But this course always asks you
to work in the challenge folder. So go back there.

### Making folders

`mkdir NAME` creates a new folder. The name means "make directory".

```console
$ mkdir songs
$ mkdir songs/old
$ ls songs
old
```

The second command used a path. It made `old` inside `songs`. The folder `songs` must exist first.

### New words

- **file**: something that holds data, like text.
- **folder / directory**: something that holds files and other folders.
- **current folder**: the folder the shell is standing in right now.
- **path**: folder names joined by `/`, like `maze/north`.
- **absolute path**: a path that starts at the root `/`. It works from any folder.
- **relative path**: a path that starts from the current folder.
- **`..`**: the folder above this one.
- **`pwd`, `ls`, `cd`, `mkdir`**: show where you are, list, move, make a folder.

## Offline help

- Offline: `man ls`, `man mkdir`, `man pwd`, and `help cd`. (cd is built into bash.)
