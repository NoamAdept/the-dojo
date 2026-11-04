# Practicing Piping

`lls-piping` · White Belt

**Goal:** Write fifteen scripts that redirect stdin, stdout and stderr to files, filter streams with `grep`, `grep -v` and `sed`, split a stream with `tee` and process substitution, and pass data through a named pipe (FIFO).

Put each answer in `answers/taskN.sh`, in place of the `TODO` line.

**Task 1**

```bash
echo PWN > COLLEGE
```

**Task 2**

```bash
"$DOJO/challenge/run" > myflag
```

**Task 3**

```bash
"$DOJO/challenge/append" >> ~/the-flag
```

**Task 4**

```bash
"$DOJO/challenge/run" > myflag 2> instructions
```

**Task 5**

```bash
echo COLLEGE > PWN
"$DOJO/challenge/needinput" < PWN
```

**Task 6**

```bash
"$DOJO/challenge/noisy" > "$DOJO/tmp/data.txt"
grep "academy{" "$DOJO/tmp/data.txt"
```

**Task 7**

```bash
"$DOJO/challenge/noisy" | grep "academy{"
```

**Task 8**

```bash
"$DOJO/challenge/noisyerr" 2>&1 | grep "academy{"
```

**Task 9**

```bash
"$DOJO/challenge/decoys" | grep -v DECOY
```

**Task 10**

```bash
"$DOJO/challenge/fakeflag" | sed "s/FAKEFLAG//g"
```

**Task 11**

```bash
"$DOJO/challenge/pwn" --secret pipeline7 | tee ~/pwn.log | "$DOJO/challenge/college"
```

**Task 12**

```bash
diff <("$DOJO/challenge/print_decoys") <("$DOJO/challenge/print_decoys_and_flag")
```

**Task 13**

```bash
"$DOJO/challenge/hack" | tee >("$DOJO/challenge/the") | "$DOJO/challenge/planet"
```

**Task 14**

```bash
"$DOJO/challenge/hack" 2> >("$DOJO/challenge/the") | "$DOJO/challenge/planet"
```

**Task 15**

```bash
mkfifo "$DOJO/tmp/flag_fifo"
"$DOJO/challenge/fifo" > "$DOJO/tmp/flag_fifo" &
cat "$DOJO/tmp/flag_fifo"
wait
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
