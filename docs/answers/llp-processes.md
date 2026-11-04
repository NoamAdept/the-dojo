# Processes and Jobs

`llp-processes` · Yellow Belt

**Goal:** Fill in six small bash scripts, `answers/task1.sh` to `answers/task6.sh`, that find, signal, pause, background and inspect processes. `./check` starts its own helper processes and runs each script against them.

Put each answer in `answers/taskN.sh`, in place of the `TODO` line.

**Task 1**

```bash
pgrep -f "$(cat target.txt)"
```

**Task 2**

```bash
pkill -f "$(cat target.txt)"
```

**Task 3**

```bash
kill -INT "$(cat pid.txt)"
```

**Task 4**

```bash
p=$(cat pid.txt)
kill -STOP "$p"
sleep 0.2
ps -o stat= -p "$p" > state.txt
kill -CONT "$p"
```

**Task 5**

```bash
./slow.sh A &
./slow.sh B &
wait
echo done
```

**Task 6**

```bash
./mystery
echo $?
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
