## Automate a Capture Inventory

*cli-shell-automation · medium*

**Goal.** Finish `inventory.sh` so `./inventory.sh DIRECTORY` writes `manifest.txt` in the current folder, with one `filename,size,sha256` line per `.iq` file, sorted by file name. The checker runs it on a fresh temporary folder that includes a name with a space.

**You need to know.**

- `$1` is the first argument; the starter already stores it in `directory`.
- A `for` loop over `"$directory"/*.iq`, with `shopt -s nullglob` for empty folders.
- `basename`, `stat -c %s` (size in bytes), `sha256sum ... | cut -d' ' -f1`.
- Quote every path variable so spaces survive.

**Walkthrough.**

1. Open `inventory.sh`. Keep the first three lines and replace the `# TODO` comment, because `./check` refuses a file that still contains `TODO`.

2. Write the loop and the sorted output. The full script:

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

   - `nullglob` makes the loop run zero times on a folder with no `.iq` files, instead of once with the literal text `*.iq`.
   - The glob `"$directory"/*.iq` keeps the folder name whole while the star still expands, and it skips `ignore.txt`.
   - `basename` drops the folder, so the line starts with just the file name.
   - `stat -c %s` prints only the byte count; `sha256sum` prints `HASH  NAME`, and `cut` keeps the hash.
   - Piping the whole loop into `sort` orders all lines by name; `LC_ALL=C` gives plain byte order, like the checker's Python `sorted`.
   - `> manifest.txt` writes into the current folder, not into the scanned one.

3. Try it by hand on a small folder.

   ```bash
   mkdir -p t && printf abc > t/alpha.iq && printf 'radio' > "t/space name.iq" && echo no > t/x.txt
   ./inventory.sh t
   cat manifest.txt
   ```

   You should see two lines, `alpha.iq,3,...` first and `space name.iq,5,...` second, and no `x.txt`.

4. Run the checker.

   ```bash
   ./check
   ```

**Check.** `./check` prints `CHECK_OK`. Then press Done.

**Common mistakes.**

- Writing `$path` without quotes, or looping over `$(ls ...)`: the file `space name.iq` splits into two words and `stat` fails.
- Printing the full path instead of the bare name, or leaving `sha256sum`'s second column in the hash.
- Leaving the `# TODO` comment in the file; the checker says "finish inventory.sh" even if the code works.
