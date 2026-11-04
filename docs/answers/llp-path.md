# Pondering PATH

`llp-path` · Yellow Belt

**Goal:** Fill in `answers/task1.sh` to `answers/task6.sh` to read PATH, find which program a name runs, add folders to PATH (for now and for every new shell), and shadow a real command with your own.

Put each answer in `answers/taskN.sh`, in place of the `TODO` line.

**Task 1**

```bash
echo "$PATH" | tr ':' '\n'
```

**Task 2**

```bash
command -v "$1"
```

**Task 3**

```bash
export PATH="$PWD/tools:$PATH"
beacon
```

**Task 4**

```bash
mkdir -p "$HOME/bin"
printf '#!/bin/bash\necho "hello from pi"\n' > "$HOME/bin/hello-pi"
chmod +x "$HOME/bin/hello-pi"
echo 'export PATH="$HOME/bin:$PATH"' >> "$HOME/.bashrc"
export PATH="$HOME/bin:$PATH"
hello-pi
```

**Task 5**

```bash
mkdir -p fake
printf '#!/bin/bash\necho 1999\n' > fake/date
chmod +x fake/date
PATH="$PWD/fake:$PATH" ./report.sh
```

**Task 6**

```bash
type -ap tool
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
