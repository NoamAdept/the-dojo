# The Locked Drawer

`orient-permissions` · Yellow Belt

**Goal:** `vault/flag.txt` has mode `----------`, so even its owner cannot read it. Give yourself read permission with `chmod`, read the flag and submit it.

Type in the challenge folder. The last line shows the flag:

```bash
ls -l vault
chmod u+r vault/flag.txt
cat vault/flag.txt
```

Paste the flag in the flag box and press **Submit**.
