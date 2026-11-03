## Namespaces and Scope Resolution

*cppq-namespaces · easy*

**Goal.** Fill `tasks.h` with seven groups of namespaces, functions and one class so that every `tests/taskN.cpp` compiles and passes.

**You need to know.**

- `namespace X { ... }` and the `::` operator (README sections 1 and 2).
- A leading `::name` always means the global name.
- C++17 nested syntax `namespace A::B::C { ... }`.
- Aliases (`namespace s = A::B;`) and `using A::B::name;` are used by the tests, so names must match exactly.

**Walkthrough.**

1. Run `./check` once. Every task says "does not compile yet", because `tasks.h` only has comments.

   ```bash
   ./check
   ```

2. Task 1, Calculator. Wrapping the functions in a namespace is all that is needed. `inline` keeps header functions safe if the header is ever included in two files.

   ```cpp
   namespace Calculator {
   inline int add(int a, int b) { return a + b; }
   inline int subtract(int a, int b) { return a - b; }
   inline int multiply(int a, int b) { return a * b; }
   }
   ```

3. Task 2, scope resolution. Three variables share the name `counter`. `inline` variables (C++17) are the header-safe way to define globals. `::counter` picks the global one.

   ```cpp
   inline int counter = 0;
   namespace Game {
   inline int counter = 10;
   namespace Player { inline int counter = 100; }
   }
   inline int sumCounters() { return ::counter + Game::counter + Game::Player::counter; }
   ```

   The test changes `Game::counter` to 11 and expects 111, so read the variables, do not hardcode 110.

4. Task 3, nested namespace in one line.

   ```cpp
   namespace Organization::HR::Payroll {
   inline double calculateSalary(double base, double bonus) { return base + bonus; }
   }
   ```

5. Task 4, two sibling namespaces inside `DataProcessing`. `average` must return 0 for an empty vector (the test calls `average({})`).

   ```cpp
   namespace DataProcessing {
   namespace Statistics {
   inline double average(const std::vector<int>& data) {
       if (data.empty()) return 0.0;
       double sum = 0.0;
       for (int v : data) sum += v;
       return sum / data.size();
   }
   inline int maximum(const std::vector<int>& data) { return *std::max_element(data.begin(), data.end()); }
   }
   namespace Formatters {
   inline std::string formatResult(const std::string& label, double value) {
       return label + ": " + std::to_string(value);
   }
   }
   }
   ```

   Add `#include <algorithm>` for `std::max_element`.

6. Task 5, Geometry. `M_PI` comes from `<cmath>` (available with g++ on Linux).

   ```cpp
   namespace Geometry {
   inline double circleArea(double r) { return M_PI * r * r; }
   inline double rectangleArea(double l, double w) { return l * w; }
   }
   ```

7. Task 6, Banking. `withdraw` refuses when funds are low, and `transferFunds` only deposits if the withdraw worked.

   ```cpp
   namespace Banking {
   class Account {
   public:
       Account(int number, double balance) : number_(number), balance_(balance) {}
       void deposit(double amount) { balance_ += amount; }
       bool withdraw(double amount) {
           if (amount > balance_) return false;
           balance_ -= amount;
           return true;
       }
       double balance() const { return balance_; }
   private:
       int number_;
       double balance_;
   };
   inline bool transferFunds(Account& from, Account& to, double amount) {
       if (!from.withdraw(amount)) return false;
       to.deposit(amount);
       return true;
   }
   }
   ```

8. Task 7, deep hierarchy. Two separate nested blocks that share the `Company::Division` prefix.

   ```cpp
   namespace Company::Division::Department::Team::Resources {
   class Employee {
   public:
       explicit Employee(std::string name) : name_(std::move(name)) {}
       std::string getInfo() const { return "Employee: " + name_; }
   private:
       std::string name_;
   };
   }
   namespace Company::Division::Finance::Accounting {
   inline double calculateBudget(double perHead, int heads) { return perHead * heads; }
   }
   ```

**Check.** `./check` prints `7/7 tasks pass` and then `CHECK_OK`. Press Done.

**Common mistakes.**

- One syntax error in `tasks.h` makes every task fail to compile, because every test includes the same header. Fix the first error first.
- Spelling or capitalisation that differs from the README (for example `Statistic` or `Formatter`): the tests use aliases and `using` with the exact names.
- Forgetting the empty-vector case in `average`, which divides by zero and returns NaN.
