# Concurrency and Networking

Write all your code in `tasks.h`. You can write inline, header-only code here. Each file in `tests/` checks one task. `./check` compiles them one at a time with `g++ -std=c++17`. So you can do the tasks in any order.

## Concurrency and Networking

Welcome to Module 14! Computers do many things at the same time, and they talk to each other.

In this module, you learn about:
1.  **Concurrency**: use threads to do several things at the same time.
2.  **Networking**: use Sockets to talk to other computers. This often needs threads too!

Is this new to you? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

1. **Racer**: write 2 functions.
   - `int racyCount(int perThread)`: 2 threads, no lock. Any result is allowed.
   - `int lockedCount(int perThread)`: uses `std::mutex`. The result is always exact.
2. **Atomic counter**: `int atomicCount(int perThread)` uses `std::atomic<int>`.
3. **Sleepy thread**: `std::vector<std::string> sleepyThread(int ms)` returns `{"Start", "End"}`. It must take at least `ms` milliseconds.
4. **Network address**: `sockaddr_in makeAddress(const char* ip, uint16_t port)`. Use `htons` and `inet_pton`.
5. **Parallel sum**: `long parallelSum(int n)` adds up the numbers 1..n. Use 2 threads and `std::ref` result variables.
6. **Port pinger**: `bool ping(const char* ip, uint16_t port)` returns true if a TCP `connect()` works. The test opens a local listening port. It also tries a closed port. No internet is used.
7. **Thread-safe queue**: `SafeQueue<T>` has 3 functions:
   - `push`
   - a blocking `pop` (it waits for an item, using `std::condition_variable`)
   - `size`

   The test runs a producer (adds items) and a consumer (takes items) at the same time.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
