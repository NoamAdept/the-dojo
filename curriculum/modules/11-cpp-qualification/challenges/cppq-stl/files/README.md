# STL Containers, Algorithms and Iterators

Write all your code in `tasks.h`. You may put all the code in the header, as inline code. Each file in `tests/` checks one task. `./check` compiles the tests one at a time with `g++ -std=c++17`. So you can do the tasks in any order.

## C++ STL: Containers, Algorithms, and Iterators

The **Standard Template Library (STL)** is a very powerful part of C++. It gives you data structures and algorithms that are fast and that you can reuse.

It has 3 main parts:
1.  **Containers**: objects that store data (for example, `vector`, `map`).
2.  **Algorithms**: functions that work on data (for example, `sort`, `find`).
3.  **Iterators**: objects that point to elements in a container. They connect algorithms with containers.

Is this new to you? Read **LESSON.md** first, or press **Lesson** in the app.

## Your tasks

1. **Vector basics**: write `float middleElement(const std::vector<float>&)`.
2. **Map phonebook**: write `std::string lookup(const std::map<std::string, std::string>& book, const std::string& name)`. If the name is missing, it returns `"not found"`.
3. **Unique words**: write `std::size_t uniqueCount(const std::vector<std::string>&)`. It uses a `std::set`.
4. **Sort descending**: write `std::vector<int> sortedDescending(std::vector<int>)`. It uses `std::greater<int>()`.
5. **Grade analyzer**: write `struct GradeReport { double average; int max; int count; };` and `GradeReport analyzeGrades(const std::vector<int>& input)`. It reads until it finds the sentinel `-1` (a special value that means "stop"). It uses `std::max_element`.
6. **Word frequency**: write `std::map<std::string, int> wordFrequency(const std::string&)`. It uses a stringstream.
7. **Custom object sort**: write `struct Player { std::string name; int score; };` and `void rankPlayers(std::vector<Player>&)`. It sorts:
   - first by score, from high to low (descending)
   - then by name, from A to Z (ascending)

   Use a lambda for this.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
