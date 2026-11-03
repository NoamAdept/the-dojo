## Extract Frequencies from Text

*cli-text-extraction · easy*

**Goal.** Pull every number written right before `MHz` out of `bulletin.txt`, drop duplicates, sort numerically, and save one number per line in `frequencies.txt`, keeping the decimals exactly as written.

**You need to know.**

- A regular expression describes the shape of the text to find (README, "Lesson").
- `grep -E` enables extended regex; `grep -o` prints only the matched part.
- `[0-9]+\.[0-9]+` means digits, a literal dot, digits.
- `sort -n -u` sorts as numbers and removes repeats.

**Walkthrough.**

1. Read the bulletin.

   ```bash
   cat bulletin.txt
   ```

   It mixes real frequencies with distractors: a time (`08:15`), `channel 12`, `ticket 2026`, and `145.800 MHz` appears twice.

2. Match only the frequency pattern.

   ```bash
   grep -Eo '[0-9]+\.[0-9]+ MHz' bulletin.txt
   ```

   Requiring a decimal point and the word `MHz` skips the time, channel and ticket. `\.` is a literal dot; a bare `.` would match any character.

3. Remove the unit.

   ```bash
   grep -Eo '[0-9]+\.[0-9]+ MHz' bulletin.txt | cut -d' ' -f1
   ```

   Each match is `NUMBER MHz`, so the first space-separated field is the number.

4. Sort, remove duplicates, and save.

   ```bash
   grep -Eo '[0-9]+\.[0-9]+ MHz' bulletin.txt | cut -d' ' -f1 | sort -n -u > frequencies.txt
   cat frequencies.txt
   ```

   The result is `28.120`, `145.800`, `162.550`, `433.500`. `sort -n` puts 28 before 145, and `-u` keeps only one `145.800`.

5. Run the checker.

   ```bash
   ./check
   ```

**Check.** `./check` prints `CHECK_OK`. Then press Done.

**Common mistakes.**

- Using plain `sort` (text order puts `145.800` before `28.120`).
- Dropping the trailing zeros, for example writing `145.8`. The checker wants the spelling from the bulletin.
- Forgetting `-E`, so `+` is treated as a literal plus sign and nothing matches.
