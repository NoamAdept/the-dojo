## STL Containers, Algorithms and Iterators

*cppq-stl · medium*

**Goal.** Use `vector`, `map`, `set`, `std::sort`, `std::max_element` and a lambda comparator to finish seven functions in `tasks.h`.

**You need to know.**

- Containers: `std::vector`, `std::map` (sorted keys), `std::set` (unique values).
- `map::find` returns `end()` when a key is missing, and does not insert (unlike `operator[]`).
- Algorithms from `<algorithm>` / `<numeric>`: `sort`, `max_element`, `accumulate`.
- A lambda can be passed to `std::sort` as the comparison.

**Walkthrough.**

1. Run `./check`, then add the includes.

   ```cpp
   #include <algorithm>
   #include <functional>
   #include <map>
   #include <numeric>
   #include <set>
   #include <sstream>
   #include <string>
   #include <vector>
   ```

2. Task 1, middle element. For 5 items, index `5 / 2 == 2` is the middle.

   ```cpp
   inline float middleElement(const std::vector<float>& v) { return v[v.size() / 2]; }
   ```

3. Task 2, phonebook. The map is `const`, so `book[name]` will not even compile; use `find`.

   ```cpp
   inline std::string lookup(const std::map<std::string, std::string>& book, const std::string& name) {
       auto it = book.find(name);
       return it == book.end() ? "not found" : it->second;
   }
   ```

4. Task 3, unique words. Building a set drops duplicates automatically.

   ```cpp
   inline std::size_t uniqueCount(const std::vector<std::string>& words) {
       return std::set<std::string>(words.begin(), words.end()).size();
   }
   ```

5. Task 4, sort descending. The vector is taken by value, so we can sort our own copy and return it.

   ```cpp
   inline std::vector<int> sortedDescending(std::vector<int> v) {
       std::sort(v.begin(), v.end(), std::greater<int>());
       return v;
   }
   ```

6. Task 5, grade analyzer. Stop at the sentinel `-1` (the `100` after it must be ignored). Start `accumulate` at `0.0` so the sum is a double.

   ```cpp
   struct GradeReport { double average; int max; int count; };

   inline GradeReport analyzeGrades(const std::vector<int>& input) {
       std::vector<int> grades;
       for (int g : input) {
           if (g == -1) break;
           grades.push_back(g);
       }
       if (grades.empty()) return {0.0, 0, 0};
       double avg = std::accumulate(grades.begin(), grades.end(), 0.0) / grades.size();
       return {avg, *std::max_element(grades.begin(), grades.end()), static_cast<int>(grades.size())};
   }
   ```

7. Task 6, word frequency. `>>` on a stringstream gives one word at a time; `counts[word]` starts at 0 for a new word.

   ```cpp
   inline std::map<std::string, int> wordFrequency(const std::string& text) {
       std::map<std::string, int> counts;
       std::istringstream in(text);
       std::string word;
       while (in >> word) ++counts[word];
       return counts;
   }
   ```

8. Task 7, custom sort. Higher score first; on a tie, alphabetical name.

   ```cpp
   struct Player { std::string name; int score; };

   inline void rankPlayers(std::vector<Player>& players) {
       std::sort(players.begin(), players.end(), [](const Player& a, const Player& b) {
           if (a.score != b.score) return a.score > b.score;
           return a.name < b.name;
       });
   }
   ```

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Using `book[name]` in `lookup`: it does not compile on a const map, and on a non-const map it would insert an empty entry.
- Averaging with an `int` start value (`accumulate(..., 0)`) gives 81 instead of 81.67.
- Forgetting the tie-break in Task 7, so `bo` and `cy` (both 50) come out in the wrong order.
