# Environment

What you will learn:

- what environment variables are,
- how to list them with printenv,
- how to join 2 of them with printf.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Goal
The flag is split into 2 environment variables inside a lab shell. Join them.

## Tools

```
./lab_shell.sh   printenv   printf
```

## Steps
1. Press Start in the dojo.

2. Go into the prepared lab shell:

```
./lab_shell.sh
```

3. List the lab variables:

```
printenv | grep '^LAB_'
```

4. Join PART1 and PART2:

```
printf '%s\n' "${LAB_FLAG_PART1}${LAB_FLAG_PART2}"
```

5. Copy the complete flag. Type exit. Then paste the flag in the dojo (or
   press Done).

Tip: reading lab_shell.sh does not show the live flag. Use the environment.
