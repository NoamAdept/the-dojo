# File Permissions

Are you new to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

Write each answer as a bash script in `answers/taskN.sh`. Each time `./check` runs, it creates the files again with new permissions.

1. **Read the modes**: print the names of the files in `box/` that *others* may read. Sort them, one per line.
2. **Symbolic chmod**: give the group write permission on `notes.txt`. Remove every permission for others. Do not change the owner bits.
3. **Octal chmod**: set `secret.txt` to `600`. Set `run.sh` to `750`.
4. **Execute bit**: make `hello.sh` executable for its owner. Then run it as `./hello.sh`.
5. **umask**: create the file `private.log` and the directory `logs`. They must come out as `640` and `750`. Use `umask` for this, not chmod.
6. **Find setuid files**: print the names of the files in `bin/` that have the setuid bit. Sort them, one per line.
7. **chgrp**: change the group of `shared.txt` to the group named in `group.txt`.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
