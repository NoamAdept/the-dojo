# Permissions: lesson

Linux keeps a small set of rules on every file. The rules say who may do
what with the file. These rules are called permissions. They are also
called the file's "mode".

There are 3 kinds of action:

```
r  read      look at what is inside
w  write     change what is inside
x  execute   run it as a program (for a folder: go inside it)
```

There are also 3 kinds of people:

```
u  user      the owner of the file (usually whoever created it)
g  group     a named team of users the file belongs to
o  other     everybody else
```

ls -l shows the rules as 10 characters at the start of each line:

```
$ ls -l notes
-rw-r----- 1 student student  42 Oct  6 10:00 diary.txt

-          first character: - is a file, d is a directory
rw-        user (owner): may read and write, may not execute
r--        group: may only read
---        other: may do nothing
```

A dash means "not allowed". Look at the 2 names after the number. The
first name is the owner. The second name is the group. Here both are
"student". The command whoami prints your own user name. So you can see
if you are the owner.

Sometimes no letter is set at all. Then you see ----------. In that case
even the owner cannot read the file:

```
$ cat notes/diary.txt
cat: notes/diary.txt: Permission denied
```

The owner of a file can always change its rules. Use chmod to do this.
chmod means "change mode". Write 3 things, with no spaces between them:

1. who (u, g or o),
2. + to add, or - to remove,
3. what (r, w or x).

```
chmod u+r diary.txt     give the owner read permission
chmod u+w diary.txt     give the owner write permission
chmod go-r diary.txt    take read away from group and other
```

Run ls -l again to check the result. stat FILE shows the same rules. It
also shows more details, if you want them.

sudo is the command that runs another command as the administrator. The
administrator is the user who may do everything. You never need sudo to
fix a file that you own. Do not use sudo in this course.

## New words
- **permissions / mode**: the rules that say who may read, write or run a file.
- **owner (user)**: the account a file belongs to.
- **group**: a named set of users that can share access.
- **other**: every user who is not the owner and not in the group.
- **chmod**: the command that changes permissions.
- **Permission denied**: the error you get when the rules say no.
- **sudo**: runs a command as the administrator (root). Not needed here.

## Offline help

- man chmod
- man ls      (look for the -l option)
