# Files and Folders

`zt-files-folders` · White Belt

**Goal:** Create the folders `radio` and `radio/notes`, save `pwd` and `ls` output into files, and find the `key-...` file hidden three folders deep in `maze`, writing its name into `key.txt`.

Type in the challenge folder:

```bash
mkdir radio
mkdir radio/notes
cd radio/notes
pwd > here.txt
cd ../..
ls maze > maze-list.txt
ls maze/north/door-3/blue
echo key-dxjakp > key.txt
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
