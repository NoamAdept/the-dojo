## OOP and Design Patterns

*cppq-oop-patterns · medium*

**Goal.** Write a small class with an invariant, a Singleton logger, an abstract `Shape` with a factory, and an Observer setup (`Sensor`, `Display`, `Alarm`) in `tasks.h`.

**You need to know.**

- `private` data plus public methods that guard it (encapsulation).
- Singleton: private constructor, `static` local instance, deleted copy.
- Pure virtual (`= 0`) makes a class abstract; a base with virtuals needs a virtual destructor.
- Observer: a subject keeps a list of `Observer*` and calls `update` on each.

**Walkthrough.**

1. Run `./check`, then include `<memory>`, `<string>` and `<vector>` in `tasks.h`.

2. Task 1, Dog. `setAge` silently ignores values outside 0 to 30, so the test's `31` and `-1` leave the age at 5.

   ```cpp
   class Dog {
   public:
       void setAge(int age) { if (age >= 0 && age <= 30) age_ = age; }
       int age() const { return age_; }
       std::string bark() const { return "Woof!"; }
   private:
       int age_ = 0;
   };
   ```

3. Task 2, Logger singleton. A function-local `static` is created once, on first use. Deleting the copy constructor is checked by a `static_assert` in the test.

   ```cpp
   class Logger {
   public:
       static Logger& instance() { static Logger logger; return logger; }
       Logger(const Logger&) = delete;
       Logger& operator=(const Logger&) = delete;
       void log(const std::string& msg) { messages_.push_back(msg); }
       int count() const { return static_cast<int>(messages_.size()); }
   private:
       Logger() = default;
       std::vector<std::string> messages_;
   };
   ```

4. Task 3, BankAccount. Refuse the withdraw before touching the balance.

   ```cpp
   class BankAccount {
   public:
       explicit BankAccount(double balance) : balance_(balance) {}
       void deposit(double amount) { balance_ += amount; }
       bool withdraw(double amount) {
           if (amount > balance_) return false;
           balance_ -= amount;
           return true;
       }
       double balance() const { return balance_; }
   private:
       double balance_;
   };
   ```

5. Task 4, abstract Shape. `= 0` makes `Shape` abstract and `virtual ~Shape()` lets a `unique_ptr<Shape>` delete a `Circle` correctly.

   ```cpp
   class Shape {
   public:
       virtual ~Shape() = default;
       virtual std::string draw() const = 0;
   };
   class Circle : public Shape { public: std::string draw() const override { return "circle"; } };
   class Square : public Shape { public: std::string draw() const override { return "square"; } };
   ```

6. Task 5, factory. The caller only knows about `Shape`; unknown names give `nullptr`.

   ```cpp
   inline std::unique_ptr<Shape> makeShape(const std::string& kind) {
       if (kind == "circle") return std::make_unique<Circle>();
       if (kind == "square") return std::make_unique<Square>();
       return nullptr;
   }
   ```

7. Task 6, Observer and Sensor. The sensor stores raw, non-owning pointers and calls each one.

   ```cpp
   class Observer {
   public:
       virtual ~Observer() = default;
       virtual void update(int value) = 0;
   };
   class Sensor {
   public:
       void attach(Observer* o) { observers_.push_back(o); }
       void notify(int value) { for (Observer* o : observers_) o->update(value); }
   private:
       std::vector<Observer*> observers_;
   };
   ```

8. Task 7, Display and Alarm. The test sends 50, 150, 99, 101: last value is 101, and two are over 100.

   ```cpp
   class Display : public Observer {
   public:
       void update(int value) override { last_ = value; }
       int last() const { return last_; }
   private:
       int last_ = 0;
   };
   class Alarm : public Observer {
   public:
       void update(int value) override { if (value > 100) ++beeps_; }
       int beeps() const { return beeps_; }
   private:
       int beeps_ = 0;
   };
   ```

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Leaving the Logger constructor public or forgetting `= delete` on the copy constructor: the `static_assert` in task 2 fails to compile.
- Forgetting the virtual destructor on `Shape`: task 4 has a `static_assert` for it.
- Writing `std::string draw()` without `const` in `Circle`: it does not override the base `draw() const`, so `Circle` stays abstract and cannot be created. Adding `override` turns this into a clear error message.
