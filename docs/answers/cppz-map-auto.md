## Lookups with std::map and auto

*cppz-map-auto · easy*

**Goal.** Fill in `countWords`, `lookup`, `totalOfValues`, `describe` and `mostCommon` in `tasks.h` using `std::map<std::string, int>` and `auto`.

**You need to know.**

- A `std::map` holds unique keys in sorted order, each with a value (README lesson).
- `m[key]` creates a missing key with value 0, which is perfect for counting but not allowed on a `const` map.
- `m.count(key)` (0 or 1) and `m.at(key)` look without changing the map.
- `for (const auto& entry : m)` visits pairs in sorted order; `entry.first` is the key, `entry.second` the value.

**Walkthrough.**

1. Task 1, `countWords` (keep the starter's `counts`):

   ```cpp
   std::map<std::string, int> counts;
   for (const auto& w : words) counts[w]++;
   return counts;
   ```

   The first time a word is seen, `counts[w]` creates it at 0, and `++` makes it 1; later times just add 1.

2. Task 2, `lookup`:

   ```cpp
   if (m.count(key) == 0) return -1;
   return m.at(key);
   ```

   `count` tells whether the key exists without adding it, so a key whose value is 0 (like `"ppm"`) still returns 0, not -1.

3. Task 3, `totalOfValues`:

   ```cpp
   int total = 0;
   for (const auto& entry : m) total += entry.second;
   return total;
   ```

   `auto` saves typing the long pair type; `.second` is the number.

4. Task 4, `describe`:

   ```cpp
   std::string out;
   for (const auto& entry : m) {
       out += entry.first + "=" + std::to_string(entry.second) + ";";
   }
   return out;
   ```

   `std::to_string` turns the int into text so it can be joined; the map already loops in sorted key order.

5. Task 5, `mostCommon`:

   ```cpp
   std::string best;
   int bestCount = 0;
   for (const auto& entry : countWords(words)) {
       if (entry.second > bestCount) {
           best = entry.first;
           bestCount = entry.second;
       }
   }
   return best;
   ```

   Reusing `countWords` does the counting. The loop goes alphabetically and only replaces on a strictly bigger count, so on a tie the earlier (alphabetically first) word stays.

6. Run `./check`.

**Check.** `./check` prints `5/5 tasks pass` and then `CHECK_OK`.

**Common mistakes.**

- `return m[key];` in `lookup`. It does not compile because `m` is `const` (and on a non-const map it would add the key).
- Using `>=` in `mostCommon`, so `"wfm"` wins the tie instead of `"nfm"`.
- Writing `entry.second` straight into a string with `+`. That does not turn the number into text; use `std::to_string`.
