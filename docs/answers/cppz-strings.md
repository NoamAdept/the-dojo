## Text with std::string

*cppz-strings · easy*

**Goal.** Fill in the five functions in `tasks.h` (`makeGreeting`, `countChar`, `isYes`, `keyOf`, `valueOf`) using `std::string` joining, comparing, indexing, `find` and `substr`.

**You need to know.**

- `+` joins strings, `==` compares them, `s[i]` reads one character, `s.size()` is the length (README lesson).
- `s.find('=')` gives the position of the first `=`, or `std::string::npos` when there is none.
- `s.substr(start, count)` cuts out a piece; `s.substr(start)` takes everything from `start` to the end.
- Each `tests/taskN.cpp` checks one function; `./check` compiles and runs them all.

**Walkthrough.**

1. Task 1, `makeGreeting`:

   ```cpp
   return "Hello, " + name + "!";
   ```

   `name` is a `std::string`, so `+` builds one new string from the three pieces.

2. Task 2, `countChar`:

   ```cpp
   int count = 0;
   for (std::size_t i = 0; i < text.size(); i++) {
       if (text[i] == c) count++;
   }
   return count;
   ```

   The loop visits positions 0 to size()-1; `std::size_t` matches the type `size()` returns, so g++ does not warn about comparing signed and unsigned.

3. Task 3, `isYes`:

   ```cpp
   return answer == "yes" || answer == "y";
   ```

   `==` compares the whole text, so `"yes please"` is false.

4. Task 4, `keyOf`:

   ```cpp
   std::size_t pos = line.find('=');
   if (pos == std::string::npos) return line;
   return line.substr(0, pos);
   ```

   `find` stops at the first `=`, and `substr(0, pos)` takes the `pos` characters before it (`"mode=fm=wide"` gives `"mode"`).

5. Task 5, `valueOf`:

   ```cpp
   std::size_t pos = line.find('=');
   if (pos == std::string::npos) return "";
   return line.substr(pos + 1);
   ```

   `pos + 1` skips the `=` itself; for `"empty="` that is the end of the string, so `substr` returns `""`.

6. Run the tests:

   ```bash
   ./check
   ```

**Check.** `./check` prints `5/5 tasks pass` and then `CHECK_OK`.

**Common mistakes.**

- Forgetting the `npos` check. `keyOf("antenna")` then works by luck but `valueOf("antenna")` returns `"antenna"` instead of `""` (npos + 1 wraps around to 0).
- Using `substr(pos)` in `valueOf`, which keeps the `=` (`"=12"`).
- Leaving the starter `return "?";` in `valueOf`: it compiles, but test 5 fails.
