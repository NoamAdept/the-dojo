# Needle in the Labyrinth

`orient-find-flag` · Yellow Belt

**Goal:** Explore the `labyrinth/` folder, skip the decoys, and read the one real flag (text shaped like `flag{...}`). Then submit it.

Type in the challenge folder. The last line shows the flag:

```bash
find . -type f
grep -r 'flag{' labyrinth
grep -rh 'flag{' labyrinth
```

Paste the flag in the flag box and press **Submit**.
