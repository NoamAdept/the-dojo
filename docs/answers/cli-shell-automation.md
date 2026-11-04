# Night Watch Inventory

`cli-shell-automation` · Yellow Belt

**Goal:** Finish `inventory.sh` so `./inventory.sh DIRECTORY` writes `manifest.txt` in the current folder, with one `filename,size,sha256` line per `.iq` file, sorted by file name. The checker runs it on a fresh temporary folder that includes a name with a space.

**File `inventory.sh`**

```bash
#!/bin/bash
set -euo pipefail
directory=${1:?Usage: ./inventory.sh DIRECTORY}

shopt -s nullglob
{
  for path in "$directory"/*.iq; do
    name=$(basename "$path")
    size=$(stat -c %s "$path")
    hash=$(sha256sum "$path" | cut -d' ' -f1)
    printf '%s,%s,%s\n' "$name" "$size" "$hash"
  done
} | LC_ALL=C sort > manifest.txt
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
