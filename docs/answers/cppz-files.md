## Reading and Writing Text Files

*cppz-files · easy*

**Goal.** Fill in `countLines`, `readLines`, `sumNumbers`, `writeLines` and `findSetting` in `tasks.h`, using `std::ifstream`, `std::ofstream` and `std::getline`.

**You need to know.**

- `std::ifstream in(path);` opens a file for reading, `std::ofstream out(path);` for writing (`<fstream>`, README lesson).
- `if (!in)` is true when the file could not be opened.
- `while (std::getline(in, line))` reads one line at a time (without the `\n`) until the end.
- `std::stoi`, `find` and `substr` from earlier challenges. Your own functions can call each other.

**Walkthrough.**

1. Task 1, `countLines`:

   ```cpp
   std::ifstream in(path);
   if (!in) return -1;
   int count = 0;
   std::string line;
   while (std::getline(in, line)) count++;
   return count;
   ```

   Each successful `getline` is one line, including empty ones, so the test file gives 5.

2. Task 2, `readLines` (keep the starter's `lines`):

   ```cpp
   std::vector<std::string> lines;
   std::ifstream in(path);
   std::string line;
   while (std::getline(in, line)) lines.push_back(line);
   return lines;
   ```

   A stream that failed to open just reads nothing, so a missing file returns an empty vector without an extra check.

3. Task 3, `sumNumbers`, built on `readLines`:

   ```cpp
   int total = 0;
   for (const auto& line : readLines(path)) {
       if (!line.empty()) total += std::stoi(line);
   }
   return total;
   ```

   Skipping empty lines matters because `std::stoi("")` throws. A missing file gives no lines and so 0.

4. Task 4, `writeLines`:

   ```cpp
   std::ofstream out(path);
   if (!out) return false;
   for (const auto& line : lines) out << line << "\n";
   return true;
   ```

   `<<` works on a file just like on `std::cout`; the file closes itself when `out` goes out of scope.

5. Task 5, `findSetting`:

   ```cpp
   for (const auto& line : readLines(path)) {
       std::size_t pos = line.find('=');
       if (pos != std::string::npos && line.substr(0, pos) == key) {
           return line.substr(pos + 1);
       }
   }
   return "";
   ```

   Comparing the whole text before `=` with `key` means `"fre"` does not match `"freq"`.

6. Run `./check`. The tests create and delete their own `tmp_taskN.txt` files in the challenge folder.

**Check.** `./check` prints `5/5 tasks pass` and then `CHECK_OK`.

**Common mistakes.**

- Not skipping empty lines in `sumNumbers`. `std::stoi("")` throws and the test program aborts.
- Matching the key with `line.find(key) == 0` (starts with). Then `findSetting(file, "fre")` wrongly returns the frequency.
- Forgetting the `if (!out) return false;` check, so writing into a missing folder still returns `true`.
