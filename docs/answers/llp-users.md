# Users and Groups

`llp-users` · Yellow Belt

**Goal:** Fill in `answers/task1.sh` to `answers/task6.sh`: three scripts that report who you are, and three that read an `/etc/passwd`-style file and pick out shells, human accounts and extra root accounts.

Put each answer in `answers/taskN.sh`, in place of the `TODO` line.

**Task 1**

```bash
whoami
```

**Task 2**

```bash
echo "$(id -u) $(id -g)"
```

**Task 3**

```bash
id -Gn | tr ' ' '\n'
```

**Task 4**

```bash
awk -F: '$7 == "/bin/bash" {print $1}' passwd.txt
```

**Task 5**

```bash
awk -F: '$3 >= 1000 && $3 != 65534 {print $1, $3}' passwd.txt | sort -k2,2n
```

**Task 6**

```bash
awk -F: '$3 == 0 {print $1}' passwd.txt
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
