# Text with std::string

**What you will learn:** how to keep text in a variable with `std::string`. You will also learn how to join, compare, measure and cut text.

Until now, your variables held one number (`int`, `double`) or one letter (`char`). Real programs also need whole pieces of text. For example: a name, a line from a file, or a setting like `freq=433`. C++ has a type for text: `std::string` (from `#include <string>`). A **string** is a piece of text. It is a row of `char`s. It grows and shrinks by itself when you change it.

```cpp
#include <iostream>
#include <string>

int main() {
    std::string name = "Ada";
    std::string greeting = "Hi, " + name + "!";   // join text with +
    std::cout << greeting << std::endl;           // Hi, Ada!
    std::cout << greeting.size() << std::endl;    // 8
    if (name == "Ada") {                          // compare with ==, no strcmp
        std::cout << "same" << std::endl;
    }
    char first = name[0];                         // 'A', the first letter
    std::cout << first << std::endl;
    return 0;
}
```

Is this new to you? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

### How this challenge works

Write your code in `tasks.h`. Every function is already there. Each one has an empty body and a comment that says what it should do. Each file in `tests/` checks one task. `./check` compiles every test with `g++ -std=c++17` and runs it. Then it tells you in plain words what is still wrong.

1. **makeGreeting**: `makeGreeting("Ada")` returns `"Hello, Ada!"`.
2. **countChar**: `countChar("banana", 'a')` returns `3`. Use a loop over the string with `size()` and `[i]`.
3. **isYes**: return `true` when the answer is exactly `"yes"` or `"y"`. Otherwise return `false`.
4. **keyOf**: return the text before the first `=`. `keyOf("freq=433")` is `"freq"`. If there is no `=`, return the whole line.
5. **valueOf**: return the text after the first `=`. `valueOf("freq=433")` is `"433"`. If there is no `=`, return `""` (empty text).

## Check your work

Run `./check` as many times as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
