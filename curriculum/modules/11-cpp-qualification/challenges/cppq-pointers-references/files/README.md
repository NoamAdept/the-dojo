# Pointers and References

Write all your code in `tasks.h`. You may put all the code in the header, as inline code. Each file in `tests/` checks one task. `./check` compiles the tests one at a time with `g++ -std=c++17`. So you can do the tasks in any order.

## C++ Pointers and References

Welcome to the fifth module! Many people find this the hardest part of C++. It is also one of the most powerful parts: **Pointers** and **References**.

Many languages, like Python or Java, manage memory for you. In C++, you can work with memory addresses directly. This gives you great power and speed. But you must also be careful.

Is this new to you? Read **LESSON.md** first, or press **Lesson** in the app.

## Your tasks

1. **Basic pointers**: write `int* addressOf(int& v)`. It returns `&v`.
2. **Modify via pointer**: write `void doubleViaPointer(int* p)`. It doubles the pointee (the value the pointer points to).
3. **Array traversal**: write `std::string walkCString(const char* s)`. It copies characters. It moves a pointer forward until it reaches `'\0'`. Do not use `strlen` or `std::string(s)`.
4. **Safety check**: write `std::string describe(const int* p)`. For nullptr it returns `"Null Pointer"`. Otherwise it returns `"Value is: <n>"`.
5. **Swapper**: write `void swap(int* a, int* b)`.
6. **Array reverser**: write `void reverseArray(int* arr, int size)`. Use 2 pointers that move toward the middle.
7. **Min/max**: write `void findMinMax(const int* arr, int size, int* minOut, int* maxOut)`. Go through the array only once (a single pass).

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
