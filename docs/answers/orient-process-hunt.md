# Ghost in the Process List

`orient-process-hunt` · Yellow Belt

**Goal:** `./run` starts a hidden background helper. Find its PID, its full start command, its working folder, the notes file named in its command, and the secret code inside that file. Write all five into `report.txt` and run `./check`.

Type in the challenge folder. The last line shows the flag:

```bash
# ./check then compares report.txt with the live helper process.
./run
sleep 1
# On a shared server other learners run helpers too: take the one started in this folder.
pid=""
for p in $(pgrep -f 'helper --work'); do
  [ "$(readlink /proc/$p/cwd 2>/dev/null)" = "$(pwd -P)" ] && pid=$p
done
cmd=$(tr '\0' ' ' < /proc/$pid/cmdline | sed 's/ $//')
notes=${cmd##*--notes }
code=$(sed -n 's/^secret_code=//p' "$notes")
cat > report.txt <<REPORT
process_number=$pid
full_command=$cmd
folder=$(readlink /proc/$pid/cwd)
notes_file=$notes
secret_code=$code
REPORT
cat report.txt
```

Paste the flag in the flag box and press **Submit**.
