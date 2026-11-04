# Pondering Paths

`lls-paths` · White Belt

**Goal:** Write eight scripts that run small programs under `$DOJO` by absolute paths, by relative paths (with and without `.`), from specific working directories, and finally with a `~/` argument.

Put each answer in `answers/taskN.sh`, in place of the `TODO` line.

**Task 1**

```bash
"$DOJO/pwn"
```

**Task 2**

```bash
"$DOJO/challenge/run"
```

**Task 3**

```bash
cd "$DOJO/var/lib/academy"
"$DOJO/challenge/position"
```

**Task 4**

```bash
cd "$DOJO/etc"
"$DOJO/challenge/tour"
cd "$DOJO/usr/share"
"$DOJO/challenge/tour"
cd "$DOJO/var/log"
"$DOJO/challenge/tour"
cd "$DOJO/home"
"$DOJO/challenge/tour"
cd "$DOJO/tmp"
"$DOJO/challenge/tour"
```

**Task 5**

```bash
cd "$DOJO"
challenge/run
```

**Task 6**

```bash
cd "$DOJO"
./challenge/run
```

**Task 7**

```bash
cd "$DOJO/challenge"
./run
```

**Task 8**

```bash
"$DOJO/challenge/copyflag" ~/f
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
