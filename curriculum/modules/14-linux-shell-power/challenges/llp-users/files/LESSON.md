# Users and Groups: lesson

Linux decides what you may do based on **who you are**. To Linux, you are 2 things:

- a user ID (**UID**), a number,
- a set of group IDs (**GIDs**), also numbers.

Names like `pi` are only labels for those numbers.

```bash
whoami     # your user name
id         # uid=1000(pi) gid=1000(pi) groups=1000(pi),27(sudo),...
id -u      # just the UID number
id -g      # just the primary GID number
id -Gn     # names of every group you are in, space separated
groups     # the same list
```

- UID `0` is **root**, the administrator.
- On most systems, UIDs below 1000 belong to services (daemons: programs that run in the
  background).
- Accounts for normal people start at 1000.
- UID 65534 is `nobody`.

**The account database.** `/etc/passwd` has 1 line for each account. Each line has 7
fields. A colon (`:`) separates the fields:

```
pi:x:1000:1000:Pi User:/home/pi:/bin/bash
1  2 3    4    5       6        7
```

1. name
2. password placeholder. The real password hashes (scrambled passwords) are in
   `/etc/shadow`. Only root can read that file.
3. UID
4. primary GID
5. comment
6. home directory
7. login shell

A shell like `/usr/sbin/nologin` means that nobody can log in to the account and type
commands.

`cut` and `awk` work very well with this format:

```bash
cut -d: -f1,7 /etc/passwd              # name and shell
awk -F: '$3 >= 1000 {print $1}' /etc/passwd   # accounts with UID 1000 or more
```

**Becoming someone else.**

- `su` switches to another user. It asks for that user's password.
- `sudo` runs 1 command as root, if an admin allowed you to do this.

These tasks do not use them. But you must understand one thing: the kernel (the core of
the operating system) only cares about the UID. So any account with UID 0 is root, with
any name. Finding extra UID 0 accounts is a classic security check.

In tasks 4 to 6, `./check` puts a new `passwd.txt` next to your script. It is different
from the example `passwd.txt` in your workspace. So read the file. Do not hard-code names
(do not write the names straight into your script).

### New words

- **UID**: user ID, the number that names a user.
- **GID**: group ID, the number that names a group.
- **primary group**: the main group of a user. New files get this group.
- **root**: the admin user (UID 0), who can do anything on the system.
- **daemon**: a program that runs in the background as a service.
- **field**: one part of a line. In `/etc/passwd`, colons separate the fields.
- **login shell**: the program that starts when the user logs in.
