# Loops over Files

**What you will learn:** how to make a script do the same thing for every file in a folder. You learn to do it safely, also when names have spaces in them.

Are you new to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

Write each answer as a bash script in `answers/taskN.sh`. `./check` runs it in a new folder with new files. So do not hard-code names (do not write the names straight into your script). `$1` and `$2` are the arguments that `./check` gives your script.

1. **First loop**: print the name of every `.txt` file in folder `$1`, one per line. Print the name without the folder part. Other files must not appear.
2. **Empty folders**: print how many `.log` files are in folder `$1`. When there are none, print `0`.
3. **Spaces survive**: copy every `.txt` file from folder `$1` into folder `$2` (it already exists). Add `.bak` to the end of each name: `$1/my notes.txt` becomes `$2/my notes.txt.bak`.
4. **Size of one file**: print only the size in bytes of the file `$1`. Its name may have spaces in it.
5. **Total size**: print the total size in bytes of all `.dat` files in folder `$1`. If there are none, print `0`.
6. **Fingerprint**: print only the sha256 hash of the file `$1`. That is 64 characters, and nothing else.
7. **Sorted report**: for every `.txt` file in folder `$1`, print `SIZE NAME`. That is the size in bytes, a space, and the name without its folder. Sort by size, smallest first.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
