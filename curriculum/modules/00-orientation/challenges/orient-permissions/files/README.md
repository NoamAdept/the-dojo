# Permissions

What you will learn:

- how to read the permission letters that ls -l shows,
- how to change them with chmod.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Goal
The flag is in vault/flag.txt. You cannot read it yet. Fix the mode bits
(the permission letters) so that you can.

## Tools

```
ls -l   chmod   cat
```

## Steps
1. Press Start in the dojo.
2. Look at the modes:

```
ls -l vault
```

3. Give your user read permission:

```
chmod u+r vault/flag.txt
```

4. Read the flag and submit it:

```
cat vault/flag.txt
```

Paste the flag in the dojo, or press Done.

You own the file. Do not use sudo. Do not delete the file. Do not change
its owner.
