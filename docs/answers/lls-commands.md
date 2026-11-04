# Comprehending Commands

`lls-commands` · White Belt

**Goal:** Write fifteen short scripts that read files (`cat`, `grep`, `diff`), list them (`ls`, `ls -a`, `find`) and change the filesystem (`touch`, `rm`, `mv`, `cp`, `mkdir`, `ln -s`), all inside the fake filesystem `$DOJO`.

Put each answer in `answers/taskN.sh`, in place of the `TODO` line.

**Task 1**

```bash
cat ~/flag
```

**Task 2**

```bash
cat "$DOJO/flag"
```

**Task 3**

```bash
cat "$DOJO/opt/vault/a1/b2/c3/flag"
```

**Task 4**

```bash
grep "academy{" "$DOJO/challenge/data.txt"
```

**Task 5**

```bash
diff "$DOJO/challenge/decoys_only.txt" "$DOJO/challenge/decoys_and_real.txt"
```

**Task 6**

```bash
ls "$DOJO/challenge"
```

**Task 7**

```bash
touch "$DOJO/tmp/pwn" "$DOJO/tmp/college"
```

**Task 8**

```bash
rm ~/delete_me
```

**Task 9**

```bash
mv "$DOJO/flag" "$DOJO/tmp/hack-the-planet"
```

**Task 10**

```bash
cp "$DOJO/flag" "$DOJO/tmp/hack-the-planet"
```

**Task 11**

```bash
ls -a "$DOJO"
```

**Task 12**

```bash
cat "$DOJO/opt/quest/.hideout/TREASURE"
```

**Task 13**

```bash
mkdir "$DOJO/tmp/pwn"
touch "$DOJO/tmp/pwn/college"
```

**Task 14**

```bash
find "$DOJO" -name flag
```

**Task 15**

```bash
ln -s "$DOJO/flag" ~/not-the-flag
"$DOJO/challenge/catflag"
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
