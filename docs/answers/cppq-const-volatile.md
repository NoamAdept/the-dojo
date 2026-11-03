## Const and Volatile Qualifiers

*cppq-const-volatile · medium*

**Goal.** Show the difference between const pointers and pointers to const, write const-correct classes with `mutable` caches, a `constexpr` size, and a `volatile` busy-wait on a fake hardware register.

**You need to know.**

- Read declarations right to left: `int* const` is "const pointer to int" (README declaration puzzle).
- A `const` reference can bind to a temporary.
- A `const` method cannot change members unless they are `mutable`.
- `constexpr` functions can run at compile time; `volatile` forces every read to really happen.

**Walkthrough.**

1. Run `./check`, then add includes: `<chrono>`, `<map>`, `<string>`, `<thread>`.

2. Task 1, declaration puzzle. The pointer itself cannot move, but the int it points to can change (the test writes `*p = 20`).

   ```cpp
   using ConstPtrToInt = int* const;
   inline int* const makeConstPtr(int& x) { return &x; }
   ```

3. Task 2, const reference. `MyData{5}` is a temporary, which only binds to `const MyData&`.

   ```cpp
   struct MyData { int val; };
   inline int printData(const MyData& d) { return d.val; }
   ```

4. Task 3, mutable cache. The test calls `heavyCalc` twice on a `const Calculator` and expects one real computation.

   ```cpp
   class Calculator {
   public:
       int heavyCalc() const {
           if (cache_ == -1) { cache_ = 42; ++computations_; }
           return cache_;
       }
       int computations() const { return computations_; }
   private:
       mutable int cache_ = -1;
       mutable int computations_ = 0;
   };
   ```

5. Task 4, constexpr. The test uses `square(5)` as an array size, which only compiles if it is a compile-time constant.

   ```cpp
   constexpr int square(int x) { return x * x; }
   constexpr int kArraySize = square(5);
   ```

6. Task 5, read-only API. `getInt` is `const`, so it must use `find`, not `operator[]` (which can insert).

   ```cpp
   class Settings {
   public:
       void setInt(const std::string& key, int val) { values_[key] = val; }
       int getInt(const std::string& key) const {
           auto it = values_.find(key);
           return it == values_.end() ? -1 : it->second;
       }
   private:
       std::map<std::string, int> values_;
   };
   ```

7. Task 6, smart cache. Only cache misses count. The test asks about 97, 97, 1, 91, 2, which is four different numbers, so `calculations()` must be 4.

   ```cpp
   class PrimeChecker {
   public:
       bool isPrime(int n) const {
           auto it = cache_.find(n);
           if (it != cache_.end()) return it->second;
           ++calculations_;
           bool prime = n >= 2;
           for (int d = 2; prime && d * d <= n; ++d) prime = n % d != 0;
           return cache_[n] = prime;
       }
       int calculations() const { return calculations_; }
   private:
       mutable std::map<int, bool> cache_;
       mutable int calculations_ = 0;
   };
   ```

8. Task 7, volatile register. One thread plays the device and writes after a delay; the other spins. `volatile` stops the compiler from reading `*reg` once and looping forever.

   ```cpp
   inline void hardwareWrite(volatile int* reg, int pattern, int delayMs) {
       std::this_thread::sleep_for(std::chrono::milliseconds(delayMs));
       *reg = pattern;
   }
   inline int waitForSignal(volatile int* reg, int pattern) {
       while (*reg != pattern) {}
       return *reg;
   }
   ```

   Tell learners that real cross-thread code should use `std::atomic<int>`; `volatile` is for memory-mapped hardware.

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Writing `const int*` (pointer to const) in Task 1: the `static_assert` and `*p = 20` both fail.
- Forgetting `mutable` on the cache: "assignment of member in read-only object" compile error.
- Dropping `volatile` from the parameter types: the test passes a `volatile int*`, so the call no longer compiles (and an optimised loop could hang, which `./check` reports as a timeout).
