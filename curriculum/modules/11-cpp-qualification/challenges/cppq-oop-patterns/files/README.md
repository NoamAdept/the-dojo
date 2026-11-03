# OOP and Design Patterns

Write all your code in `tasks.h`. You may put all the code in the header, as inline code. Each file in `tests/` checks one task. `./check` compiles the tests one at a time with `g++ -std=c++17`. So you can do the tasks in any order.

## OOP and Design Patterns

Welcome to Module 3! In this challenge, you start **Object-Oriented Programming (OOP)**. You also learn how to structure it with **Design Patterns**.

Is this new to you? Read **LESSON.md** first, or press **Lesson** in the app.

## Your tasks

1. **Class basics**: write a class `Dog` with:
   - a private age
   - `setAge(int)`. It only accepts 0–30. It ignores other values.
   - `age()`
   - `bark()`, which returns `"Woof!"`
2. **Logger singleton**: write a `Logger` with:
   - `Logger::instance()`. It returns the same object every time.
   - `log(msg)`. It stores the message.
   - `count()`. It returns how many messages are stored.
   - copy construction deleted (nobody can copy a Logger).
3. **Bank account**: write `BankAccount(double)` with `deposit` and `withdraw`. If the balance would go below zero, `withdraw` returns false and does not change the balance.
4. **Abstract shape**: write a class `Shape`. It has a pure virtual `std::string draw() const` and a virtual destructor. Then write `Circle`, which returns `"circle"`, and `Square`, which returns `"square"`.
5. **Shape factory**: write `std::unique_ptr<Shape> makeShape(const std::string&)`. For a name it does not know, it returns `nullptr`.
6. **Observer interface**: write an `Observer` base class with `virtual void update(int value) = 0`. Also write `Sensor` with `attach(Observer*)` and `notify(int)`.
7. **Display and alarm**: write 2 observers:
   - `Display` remembers the last value (`last()`).
   - `Alarm` counts readings over 100 (`beeps()`).

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
