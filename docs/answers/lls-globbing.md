# File Globbing

`lls-globbing` · White Belt

**Goal:** Write ten scripts that use the glob characters `*`, `?`, `[]` and `[!]` to hand programs the right file names, and use `compgen` to print what Tab completion would offer.

Put each answer in `answers/taskN.sh`, in place of the `TODO` line.

**Task 1**

```bash
cd "$DOJO"/ch*
"$DOJO/challenge/run"
```

**Task 2**

```bash
cd "$DOJO"/?ha??enge
"$DOJO/challenge/run"
```

**Task 3**

```bash
cd "$DOJO/challenge/files"
"$DOJO/challenge/run" file_[absh]
```

**Task 4**

```bash
"$DOJO/challenge/run" "$DOJO"/challenge/files/file_[absh]
```

**Task 5**

```bash
cd "$DOJO/challenge/words"
"$DOJO/challenge/run" *p*
```

**Task 6**

```bash
cd "$DOJO/challenge/words"
"$DOJO/challenge/run" [cep]*
```

**Task 7**

```bash
cd "$DOJO/challenge/words"
"$DOJO/challenge/run" [!pwn]*
```

**Task 8**

```bash
compgen -f "$DOJO/challenge/pwnc"
```

**Task 9**

```bash
compgen -f "$DOJO/challenge/tabfiles/pwncollege-f"
```

**Task 10**

```bash
compgen -c pwncollege | sort -u
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
