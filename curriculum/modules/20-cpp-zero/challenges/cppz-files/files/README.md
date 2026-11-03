# Reading and Writing Text Files

**What you will learn:** how to read a text file line by line. You will also learn how to write a text file. You will do both the C++ way.

Programs often need to keep data after they stop. They also often read data that someone else saved. For example: settings, recorded samples, or logs. This data is kept in **files**. C++ reads and writes files with file **streams** from `#include <fstream>`. A stream is something you read from or write to, in order. File streams work like `std::cout`, but for files.

Is this new to you? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

### How this challenge works

Write your code in `tasks.h`. Every function is already there. Each one has an empty body and a comment that says what it should do. Each file in `tests/` checks one task. `./check` compiles every test with `g++ -std=c++17` and runs it. Then it tells you in plain words what is still wrong.

1. **countLines**: return the number of lines in the file. If the file cannot be opened, return `-1`.
2. **readLines**: return all lines of the file as a `std::vector<std::string>`, in order. If the file cannot be opened, return an empty vector.
3. **sumNumbers**: the file has one whole number on each line. Return the sum of the numbers. Skip empty lines. If the file cannot be opened, return 0.
4. **writeLines**: write each string to the file on its own line. End every line with `"\n"`. If the file cannot be created, return `false`. Otherwise return `true`.
5. **findSetting**: the file has lines like `gain=30`. Return the value for `key` as text (`"30"`). If no line has that key, return `""`. Use what you learned about `find` and `substr`.

## Check your work

Run `./check` as many times as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
