# Find the Flag: lesson

A "flag" is a piece of secret text. It proves that you solved a challenge.
In this course, every flag has the same shape:

1. the word flag,
2. an opening curly brace,
3. some words joined by underscores,
4. a closing curly brace.

When you see text with that shape, you have found a flag.

Folders are also called directories. A folder can sit inside another
folder, like a box inside a box. The shell always "stands" in one folder.
This folder is called the current working directory.

```
pwd        print the folder you are standing in
           $ pwd
           /home/student/orient-find-flag

ls         list what is in this folder
           $ ls
           NOTES.txt  README.md  labyrinth

ls -la     list everything, in long form, including hidden entries
           -l means "long" (one entry per line, with details)
           -a means "all" (also show hidden entries)

           $ ls -la
           drwxr-xr-x  3 student student 4096 Oct  6 10:00 .
           drwxr-xr-x 20 student student 4096 Oct  6 10:00 ..
           -rw-r--r--  1 student student  180 Oct  6 10:00 NOTES.txt
           drwxr-xr-x  5 student student 4096 Oct  6 10:00 labyrinth

           A line starting with d is a directory. A line starting with -
           is a normal file. The name is the last column.
```

A hidden file or folder is a file or folder whose name starts with a dot.
Examples are .cache and .secret. Plain ls does not show them. ls -a shows
them. People often hide things this way. So always use -a when you search.

Every folder has 2 special names:

- . means "this folder".
- .. means "the folder above".

So cd .. moves you up one level.

```
cd labyrinth      walk into the labyrinth folder
cd ..             walk back up
cat NOTES.txt     print the contents of a file to the screen
```

Walking from folder to folder is slow. The find command walks the whole
tree (all folders inside folders) for you:

```
find . -type f              every file under here (. = start here)
find . -name '*.txt'        only names ending in .txt
find . -name '*key*'        only names containing "key"
```

Here is some example output. Each path starts from the folder where you
ran find:

```
$ find . -type f
./NOTES.txt
./labyrinth/somewhere/thing.txt
```

find also lists hidden files. It also lists files inside hidden folders.
Copy a path that find prints. Then give it to cat to read the file.

Be careful: some files are decoys (fakes). Read each file you open. Make
sure it really is a flag.

## New words
- **flag**: the secret text that proves you solved a challenge.
- **directory / folder**: a container for files and other folders.
- **current working directory**: the folder the shell is standing in.
- **hidden file**: a file whose name starts with a dot.
- **path**: the route to a file. It is folder names joined by slashes.
- **. and ..**: "this folder" and "the folder above".
- **decoy**: a fake that looks like the real thing.
- **tree**: a folder with all the folders and files inside it.

## Offline help

- man find        (offline: the full find manual, press q to quit)
- man ls
