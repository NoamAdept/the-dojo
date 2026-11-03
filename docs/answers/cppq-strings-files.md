## Strings and Files

*cppq-strings-files · easy*

**Goal.** Write seven small string and file helpers in `tasks.h`: formatting, `stoi`, writing and reading text files, a CSV parser and a line/word/character counter.

**You need to know.**

- `std::string` concatenation, `find` and `substr` (README string sections).
- `std::stoi` and `std::stod` to turn text into numbers.
- `std::ofstream` / `std::ifstream`, `is_open()` and `std::getline`.
- `std::istringstream` with `>>` splits on any whitespace.

**Walkthrough.**

1. Run `./check` to see all seven tasks fail. Add the includes you need at the top of `tasks.h`.

   ```cpp
   #include <fstream>
   #include <sstream>
   #include <string>
   ```

2. Task 1, string formatting. Build the sentence from pieces; note the comma and the final full stop.

   ```cpp
   inline std::string bondName(const std::string& first, const std::string& last) {
       return last + ", " + first + " " + last + ".";
   }
   ```

3. Task 2, number parsing. `std::stoi` handles the minus sign too (`"-7"` gives 43).

   ```cpp
   inline int addFifty(const std::string& s) { return std::stoi(s) + 50; }
   ```

4. Task 3, logger. Opening a file in a missing folder fails, so check `is_open()` and return false.

   ```cpp
   inline bool writeLog(const std::string& path, const std::string& message) {
       std::ofstream out(path);
       if (!out.is_open()) return false;
       out << message << "\n";
       return true;
   }
   ```

5. Task 4, file reader. If the file does not exist the stream is false, so `line` stays empty.

   ```cpp
   inline std::string readFirstLine(const std::string& path) {
       std::ifstream in(path);
       std::string line;
       if (in) std::getline(in, line);
       return line;
   }
   ```

6. Task 5, profile saver. Write the exact format, then reuse `readFirstLine` to verify. The temporary `ofstream` is closed (and flushed) at the end of the statement.

   ```cpp
   inline void saveProfile(const std::string& path, const std::string& name, int age) {
       std::ofstream(path) << "Name: " << name << ", Age: " << age << "\n";
   }
   inline bool verifyProfile(const std::string& path, const std::string& name, int age) {
       return readFirstLine(path) == "Name: " + name + ", Age: " + std::to_string(age);
   }
   ```

7. Task 6, CSV parser. Find the two commas, cut three pieces, convert the last two. Names may contain spaces (`"Raspberry Pi 5 kit"`), so split on commas, not with `>>`.

   ```cpp
   struct Product { std::string name; double price; int quantity; };

   inline Product parseProduct(const std::string& csv) {
       std::size_t a = csv.find(','), b = csv.find(',', a + 1);
       return {csv.substr(0, a), std::stod(csv.substr(a + 1, b - a - 1)), std::stoi(csv.substr(b + 1))};
   }
   inline double totalValue(const Product& p) { return p.price * p.quantity; }
   ```

8. Task 7, text statistics. `getline` strips the newline, so `line.size()` already excludes it. An `istringstream` per line counts words and ignores double spaces.

   ```cpp
   struct TextStats { int lines; int words; int characters; };

   inline TextStats fileStats(const std::string& path) {
       TextStats s{0, 0, 0};
       std::ifstream in(path);
       std::string line, word;
       while (std::getline(in, line)) {
           ++s.lines;
           s.characters += static_cast<int>(line.size());
           std::istringstream words(line);
           while (words >> word) ++s.words;
       }
       return s;
   }
   ```

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Writing the log without checking `is_open()`: the test for `/no/such/dir/log.txt` then wrongly gets `true`.
- Counting characters with the newline included, or counting words with `find(' ')`, which breaks on `"fox  jumps"` (two spaces) and on the empty line.
- Using `substr(a + 1, b)` instead of `substr(a + 1, b - a - 1)`: the second argument is a length, not an end index.
