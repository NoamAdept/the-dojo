# RAII and Smart Pointers

Write all your code in `tasks.h`. You may put all the code in the header, as inline code. Each file in `tests/` checks one task. `./check` compiles the tests one at a time with `g++ -std=c++17`. So you can do the tasks in any order.

## C++ Memory Management: RAII and Smart Pointers

Welcome to Module 8! This is a very important step in learning C++.

In Module 5, you saw raw pointers. They are powerful, but they are dangerous:
- If you forget to free memory, you get **Memory Leaks**.
- If you free it too early, you get **Crashes**.

Modern C++ (C++11 and later) fixes this with **RAII** and **Smart Pointers**. In modern C++ code, you should almost **never** write `new` and `delete` by hand.

Is this new to you? Read **LESSON.md** first, or press **Lesson** in the app.

## Your tasks

In these tasks, destructors write events into a global log. This lets the tests see when objects die. `tests/check.h` does not give you this log. So declare `inline std::vector<std::string> g_events;` in `tasks.h`.

1. **Unique pointer**: write a `Widget`. Its constructor pushes `"built"` to `g_events`. Its destructor pushes `"broken"`. Also write `std::unique_ptr<Widget> makeWidget()`.
2. **Moving ownership**: write `int takeOwnership(std::unique_ptr<int> p)`. It returns `*p`. The caller must use `std::move` to pass the pointer in.
3. **Shared counting**: write `long sharedCountDemo()`. Inside a scope that holds a copy, read `use_count()`. Return that value (2).
4. **RAII tracer**: write `ScopeLogger(name)`. It pushes `"Enter: name"` and `"Exit: name"`.
5. **Smart factory**: write `std::unique_ptr<int> createObject(int value)`.
6. **Linked list**: write these:
   - `struct Node { int data; std::unique_ptr<Node> next; };`
   - `std::unique_ptr<Node> makeChain(const std::vector<int>&)`
   - `std::vector<int> traverse(const Node*)`
7. **Resource manager**: write `FileManager(name)`. It pushes `"Opening <name>"` and `"Closing <name>"`. Its `write(msg)` pushes `msg`.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
