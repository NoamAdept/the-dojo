# Chaining Commands and Scripts

`llp-chaining` · Yellow Belt

**Goal:** Fill in `answers/task1.sh` to `answers/task7.sh`: three one-line chains with `;`, `&&` and `||`, three small scripts that use arguments and `if`, and one script that writes an executable `./hello`.

Put each answer in `answers/taskN.sh`, in place of the `TODO` line.

**Task 1**

```bash
./first ; ./second
```

**Task 2**

```bash
./build && ./deploy
```

**Task 3**

```bash
./primary || ./backup
```

**Task 4**

```bash
echo "$2 $1"
echo "$#"
```

**Task 5**

```bash
if [ -f "$1" ]; then
    echo "found $1"
else
    echo "missing $1"
    exit 1
fi
```

**Task 6**

```bash
if [ "$1" -lt 0 ]; then
    echo negative
elif [ "$1" -eq 0 ]; then
    echo zero
elif [ "$1" -lt 10 ]; then
    echo small
else
    echo large
fi
```

**Task 7**

```bash
cat > hello <<'EOF'
#!/bin/bash
echo "Hello, $1!"
EOF
chmod +x hello
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
