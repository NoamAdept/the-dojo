# Running Programs and Reading Errors

`zt-run-programs` · White Belt

**Goal:** Run four small programs in the challenge folder, fix the three classic errors (`command not found`, `Permission denied`, `No such file or directory`), and save each program's output into a file. Then fix `config.txt` until `./checkme` prints `ALL GOOD`.

**File `config.txt`**

```text
name=pi-radio
band=fm
gain=10
```

**File `data/settings.txt`**

```text
volume=7
```

Then type:

```bash
./greet > greet.txt
chmod +x locked
./locked > locked.txt
./report > report.txt
./checkme
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
