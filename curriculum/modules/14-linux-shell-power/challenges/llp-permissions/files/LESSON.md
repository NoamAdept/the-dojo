# File Permissions: lesson

Every file has an **owner** (a user), a **group** (a set of users) and 3 sets of
permission bits. A permission bit is a yes/no switch for one right. `ls -l` shows them:

```
-rwxr-x---  1 pi radio  812 Oct  6 10:00 tune.sh
^\_/\_/\_/     ^  ^
| u  g  o     |  group
type          owner
```

The letters mean:

- `r`: read.
- `w`: write.
- `x`: execute (run). For a directory, `x` means you may enter it.

The 3 sets are for different people:

- `u`: the owner (user).
- `g`: the group.
- `o`: everyone else (others).

Each set is also a digit. Add r=4, w=2, x=1. So `rwxr-x---` is `750`.
`stat -c %a FILE` prints that number directly.

**chmod, symbolic.** Say who, then `+`/`-`/`=`, then which bits. It changes only the bits
that you name.

```bash
chmod u+x tune.sh        # owner may execute
chmod g+w,o-rwx log.txt  # group may write, others get nothing
chmod a=r notes.txt      # everyone read only
```

**chmod, octal.** Set all bits at once with a number: `chmod 600 secret.key`. This means
only the owner can read and write.

**The execute bit** lets you run `./script.sh`. Without it, you get "Permission
denied". But `bash script.sh` still works, because bash only needs to read the file.

**umask** decides the permissions of *new* files. New files start from `666`. New
directories start from `777`. Then the bits in the umask are removed.

- The usual umask `022` gives `644` files and `755` directories.
- `umask 077` makes everything private.

The umask applies to the current shell and to the programs it starts.

**Special bits.** You can add a 4th digit at the front. It adds setuid (4), setgid (2)
and sticky (1).

**setuid** on a program means the program runs with the UID (user ID) of the *file
owner*, not with yours. That is how `passwd` can update `/etc/shadow`: root owns
`passwd`, and its mode is `4755`. In `ls -l` setuid shows as an `s` in the place of the
owner's `x`: `-rwsr-xr-x`. setuid root programs are powerful. So finding them
(`find / -perm -4000`) is a standard security check.

**Owner and group.**

- `chown` changes the owner. Only root (the admin user) can do it.
- `chgrp` changes the group. A normal user may do it for their own files. The new group
  must be a group they belong to (see `id -Gn`).

### New words

- **owner / group / others**: the 3 kinds of people that permissions are set for.
- **permission bit**: a yes/no switch for one right, like read or write.
- **symbolic mode**: permissions written with letters, like `g+w`.
- **octal mode**: permissions written as digits from 0 to 7, like `750`.
- **umask**: a mask of bits that are removed from every new file and directory.
- **setuid**: a special bit. The program runs as its owner, not as you.
- **UID**: user ID, the number that names a user.
- **root**: the admin user, who can do anything on the system.
