# Users and Groups

Are you new to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

Write each answer as a bash script in `answers/taskN.sh`.

1. **whoami**: print your user name.
2. **Numbers**: print your UID and your primary GID on 1 line, with a space between them (for example `1000 1000`).
3. **Groups**: print the names of all groups you belong to, one per line.
4. **Bash users**: look in `passwd.txt`. Print the names of the accounts whose login shell is exactly `/bin/bash`. Keep the order of the file.
5. **Human accounts**: look in `passwd.txt`. Print `name uid` for every account with UID 1000 or more. Leave out `nobody` (65534). Sort by UID, smallest first.
6. **Root audit**: look in `passwd.txt`. Print the names of every account with UID 0. Keep the order of the file.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
