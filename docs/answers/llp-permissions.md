# File Permissions

`llp-permissions` · Yellow Belt

**Goal:** Fill in `answers/task1.sh` to `answers/task7.sh` to read modes, change them with symbolic and octal `chmod`, use the execute bit, `umask`, find setuid files and change a file's group. `./check` creates the files with fresh permissions on every run.

Put each answer in `answers/taskN.sh`, in place of the `TODO` line.

**Task 1**

```bash
find box -type f -perm -o=r -printf '%f\n' | sort
```

**Task 2**

```bash
chmod g+w,o-rwx notes.txt
```

**Task 3**

```bash
chmod 600 secret.txt
chmod 750 run.sh
```

**Task 4**

```bash
chmod u+x hello.sh
./hello.sh
```

**Task 5**

```bash
umask 027
touch private.log
mkdir logs
```

**Task 6**

```bash
find bin -type f -perm -4000 -printf '%f\n' | sort
```

**Task 7**

```bash
chgrp "$(cat group.txt)" shared.txt
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
