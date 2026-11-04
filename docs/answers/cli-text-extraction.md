# Frequencies in the Fog

`cli-text-extraction` · Yellow Belt

**Goal:** Pull every number written right before `MHz` out of `bulletin.txt`, drop duplicates, sort numerically, and save one number per line in `frequencies.txt`, keeping the decimals exactly as written.

Type in the challenge folder:

```bash
grep -Eo '[0-9]+\.[0-9]+ MHz' bulletin.txt | cut -d' ' -f1 | sort -n -u > frequencies.txt
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
