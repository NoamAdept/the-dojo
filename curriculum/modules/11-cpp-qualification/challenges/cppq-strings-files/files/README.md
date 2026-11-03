# Strings and Files

Write all your code in `tasks.h`. You may put all the code in the header, as inline code. Each file in `tests/` checks one task. `./check` compiles the tests one at a time with `g++ -std=c++17`. So you can do the tasks in any order.

## C++ Data Handling: Strings and Files

Welcome to Module 2! So far, you have mostly worked with numbers and volatile memory. (Volatile memory loses its data when the power goes off.)

Real programs also need to:
1.  Work with text (user names, messages, logs).
2.  Save data so it stays after the program ends (files).

In this challenge, you learn `std::string` and File I/O (`fstream`).

Is this new to you? Read **LESSON.md** first, or press **Lesson** in the app.

## Your tasks

1. **String formatting**: write `std::string bondName(first, last)`. For `("James", "Bond")` it returns `"Bond, James Bond."`.
2. **Number parsing**: write `int addFifty(const std::string& s)`. It uses `std::stoi`.
3. **Simple logger**: write `bool writeLog(path, message)`. It writes one line to the file. If it cannot open the file, it returns false.
4. **File reader**: write `std::string readFirstLine(path)`. If the file is missing, it returns `""`.
5. **Profile saver**: write 2 functions:
   - `saveProfile(path, name, age)` writes `Name: John, Age: 30`.
   - `bool verifyProfile(path, name, age)` reads the file back and compares.
6. **CSV parser**: write these:
   - `struct Product { std::string name; double price; int quantity; };`
   - `Product parseProduct(const std::string& csv)`
   - `double totalValue(const Product&)`
7. **Text statistics**: write `struct TextStats { int lines; int words; int characters; };` and `TextStats fileStats(path)`. It counts:
   - lines
   - words (split on whitespace)
   - characters (do not count newlines)

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
