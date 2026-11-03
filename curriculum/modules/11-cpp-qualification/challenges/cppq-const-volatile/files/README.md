# Const and Volatile Qualifiers

Write all your code in `tasks.h`. You may put all the code in the header, as inline code. Each file in `tests/` checks one task. `./check` compiles the tests one at a time with `g++ -std=c++17`. So you can do the tasks in any order.

## C++ Const and Volatile Qualifiers

Welcome to Module 4! In C++, you can tell the compiler a lot about how variables should behave. You do this with **Qualifiers**.

They describe safety, what you mean, and what is really true:
1.  **`const`**: "I promise not to change this value."
2.  **`volatile`**: "This value might change when you do not expect it (for example, hardware changes it)."

Is this new to you? Read **LESSON.md** first, or press **Lesson** in the app.

## Your tasks

1. **Declaration puzzle**: write `int* const makeConstPtr(int& x)`. Then define `using ConstPtrToInt = int* const;`. This is a constant pointer to a mutable (changeable) int.
2. **Const correctness**: write `struct MyData { int val; }` and `int printData(const MyData&)`. It returns `val`. Because the parameter is a const reference, you can pass a temporary such as `MyData{5}`.
3. **Mutable cache**: write `Calculator::heavyCalc() const`. It computes 42 only once and caches (saves) it in a `mutable` member. `computations()` counts how many real computations happened.
4. **Constexpr size**: write `constexpr int square(int)` and `constexpr int kArraySize = square(5);`.
5. **Read-only API**: write `Settings` with `setInt(key, val)` and a const `getInt(key)`. For a missing key, `getInt` returns -1.
6. **Smart cache**: write `PrimeChecker::isPrime(int) const`. It uses a `mutable std::map<int,bool>` cache. `calculations()` counts the cache misses (times the answer was not in the cache).
7. **Hardware register**: write 2 functions:
   - `int waitForSignal(volatile int* reg, int pattern)` busy-waits (loops and checks again and again) until `*reg == pattern`. Then it returns the value.
   - `void hardwareWrite(volatile int* reg, int pattern, int delayMs)` sleeps and then writes. It acts like a device.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
