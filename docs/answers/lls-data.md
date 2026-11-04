# Data Manipulation

`lls-data` · White Belt

**Goal:** Write six one-line pipelines that clean up a program's output with `tr`, `head`, `cut` and `sort` so that only the secret (or the right input) comes out.

Put each answer in `answers/taskN.sh`, in place of the `TODO` line.

**Task 1**

```bash
"$DOJO/challenge/swapcase" | tr a-zA-Z A-Za-z
```

**Task 2**

```bash
"$DOJO/challenge/carets" | tr -d "^%"
```

**Task 3**

```bash
"$DOJO/challenge/newlines" | tr -d "\n"
```

**Task 4**

```bash
"$DOJO/challenge/pwn" | head -n 7 | "$DOJO/challenge/college"
```

**Task 5**

```bash
"$DOJO/challenge/columns" | cut -d " " -f 2 | tr -d "\n"
```

**Task 6**

```bash
sort "$DOJO/challenge/flags.txt" | tail -n 1
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
