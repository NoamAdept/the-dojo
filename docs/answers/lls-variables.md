# Shell Variables

`lls-variables` · White Belt

**Goal:** Write eight scripts that print, set, quote and export variables, filter `env`, store a command's output in a variable, and fill a variable with `read` from stdin and from a file.

Put each answer in `answers/taskN.sh`, in place of the `TODO` line.

**Task 1**

```bash
echo "$FLAG"
```

**Task 2**

```bash
PWN=COLLEGE
```

**Task 3**

```bash
PWN="COLLEGE YEAH"
```

**Task 4**

```bash
export PWN=COLLEGE
COLLEGE=PWN
"$DOJO/challenge/run"
```

**Task 5**

```bash
env | grep "^FLAG="
```

**Task 6**

```bash
PWN=$("$DOJO/challenge/secret")
```

**Task 7**

```bash
read PWN
```

**Task 8**

```bash
read PWN < "$DOJO/challenge/read_me"
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
