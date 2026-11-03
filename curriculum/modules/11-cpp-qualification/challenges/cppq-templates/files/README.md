# Templates and Generic Programming

Write all your code in `tasks.h`. You can write inline, header-only code here. Each file in `tests/` checks one task. `./check` compiles them one at a time with `g++ -std=c++17`. So you can do the tasks in any order.

## C++ Templates and Generic Programming

Welcome to Module 15! Templates make C++ very flexible.

Imagine you write a `swap` function for `int`. Then another one for `float`. Then another one for `double`. You write the same code again and again!

**Generic Programming** lets you write code that works with *any* data type. In C++, we do this with **Templates**.

Is this new to you? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

1. **Generic swap**: `template <class T> void mySwap(T& a, T& b)`.
2. **Generic adder**: `template <class T> T add(T a, T b)` works for int and also for `std::string`.
3. **Wrapper class**: `Holder<T>` has:
   - a private `content`
   - a constructor
   - `get()`
   - `display()`, which returns the content as a string. Use `std::ostringstream`.
4. **Triplets**: `template <class A, class B, class C> std::string printTriplet(A, B, C)` returns `"(a, b, c)"`.
5. **Max finder**: `template <class T> const T& myMax(const T& a, const T& b)` uses `>`.
6. **Generic pair**: `MyPair<K, V>` has:
   - public `key` and `value`
   - a constructor
   - `print()`, which returns `"Key: k, Value: v"`
7. **Generic stack**: `Stack<T>` stores its items in a `std::vector<T>`.
   - It has `push`, `pop`, `top` and `isEmpty`.
   - `top()` and `pop()` on an empty stack throw `std::out_of_range`.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
