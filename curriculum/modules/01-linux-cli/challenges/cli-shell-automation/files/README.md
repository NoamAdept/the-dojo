# Shell Automation

What you will learn: how to write a small bash script. The script will:

- take an argument,
- loop over files,
- get the size and the fingerprint (hash) of each file,
- write sorted lines to a file.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Goal
Finish inventory.sh. It must build a manifest (a list) of .iq files.

## Deliverable
- **Running**: `./inventory.sh DIRECTORY`
- **Creates**: `manifest.txt` in the current directory
- **Lines**: `filename,size,sha256` (only .iq files, sorted by name)

## Steps
1. Press Start and open inventory.sh.
2. Write the script so it works as shown under Deliverable.
3. Prove that it works:

```
./check
```

   The check uses a new temporary directory. So your script must work
   with any directory, not only the example files.

4. When the check passes, press Done.
