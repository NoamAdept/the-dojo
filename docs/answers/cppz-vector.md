## Lists with std::vector

*cppz-vector · easy*

**Goal.** Fill in `sumAll`, `countAbove`, `makeRange`, `largest` and `longWords` in `tasks.h` using `std::vector`, `push_back` and range-based `for`.

**You need to know.**

- `std::vector<int>` is a list that knows its `size()` and grows with `push_back` (README lesson).
- `for (int x : v)` visits every item in order, with no index to get wrong.
- A function can build a vector and return it.
- The accumulator pattern from cpf-loops (a total or count that starts before the loop).

**Walkthrough.**

1. Task 1, `sumAll`:

   ```cpp
   int total = 0;
   for (int x : v) total += x;
   return total;
   ```

   For an empty vector the loop runs zero times and 0 is returned.

2. Task 2, `countAbove`:

   ```cpp
   int count = 0;
   for (int x : v) {
       if (x > limit) count++;
   }
   return count;
   ```

   "Bigger than" means `>`, so values equal to `limit` are not counted.

3. Task 3, `makeRange` (keep the starter's `out` and fill it):

   ```cpp
   std::vector<int> out;
   for (int i = 1; i <= n; i++) out.push_back(i);
   return out;
   ```

   For `n` of 0 or less the condition is false at once, so the empty vector comes back.

4. Task 4, `largest`:

   ```cpp
   int best = v[0];
   for (int x : v) {
       if (x > best) best = x;
   }
   return best;
   ```

   Starting from `v[0]` (a real item) works for all-negative lists; starting from 0 would wrongly return 0.

5. Task 5, `longWords`:

   ```cpp
   std::vector<std::string> out;
   for (std::string w : words) {
       if (w.size() >= minLen) out.push_back(w);
   }
   return out;
   ```

   Walking `words` in order and appending keeps the original order. `minLen` is a `std::size_t`, the same type as `w.size()`.

6. Run `./check`.

**Check.** `./check` prints `5/5 tasks pass` and then `CHECK_OK`.

**Common mistakes.**

- `int best = 0;` in `largest`. The test with `{-8, -3, -12}` then gets 0 instead of -3.
- Off-by-one in `makeRange`: `for (int i = 0; i < n; i++)` gives `{0, 1, 2, 3, 4}`.
- Using `>` instead of `>=` in `longWords`, which drops `"sdr"` (exactly 3 letters).
