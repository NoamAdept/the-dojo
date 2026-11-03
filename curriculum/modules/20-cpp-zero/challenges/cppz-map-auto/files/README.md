# Lookups with std::map and auto

**What you will learn:** how to store "name to value" pairs in a `std::map`. You will also learn how `auto` saves you from typing long type names.

A **map** is like a phone book. You look up a **key** (a name) and get a **value** (a number). C++ has `std::map` (from `#include <map>`):

```cpp
#include <map>
#include <string>

std::map<std::string, int> ages;   // keys are strings, values are ints
ages["ada"] = 36;                  // add or change a value
ages["bob"] = 41;
std::cout << ages["ada"] << std::endl;   // 36
std::cout << ages.size() << std::endl;   // 2
```

There are 2 types in the angle brackets. The first is the key type. The second is the value type. Each key can be in the map only once.

Is this new to you? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

### How this challenge works

Write your code in `tasks.h`. Every function is already there. Each one has an empty body and a comment that says what it should do. Each file in `tests/` checks one task. `./check` compiles every test with `g++ -std=c++17` and runs it. Then it tells you in plain words what is still wrong.

1. **countWords**: return a map. Each key is a word. Its value is the number of times the word appears. `countWords({"fm", "am", "fm"})` gives `{"am": 1, "fm": 2}`.
2. **lookup**: return the value for `key`. If the key is not in the map, return `-1`. The map is `const`, so use `count` and `at`.
3. **totalOfValues**: return the sum of all values. Loop with `for (const auto& entry : m)`.
4. **describe**: write every pair as `key=value;` and join them all together. Use the order of the map (sorted order). For `{"am": 1, "fm": 2}` that is `"am=1;fm=2;"`. An empty map gives `""`.
5. **mostCommon**: return the word that appears most often in the list. Two words can have the same count (a tie). Then return the word that comes first in alphabetical order. The list is never empty. Hint: use your `countWords`.

## Check your work

Run `./check` as many times as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
