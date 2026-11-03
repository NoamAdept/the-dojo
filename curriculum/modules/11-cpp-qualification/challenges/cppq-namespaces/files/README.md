# Namespaces and Scope Resolution

Write all your code in `tasks.h`. You may put all the code in the header, as inline code. Each file in `tests/` checks one task. `./check` compiles the tests one at a time with `g++ -std=c++17`. So you can do the tasks in any order.

## Namespaces and Scope Resolution in C++

Welcome to Module 1! In this challenge, you learn one of the basic ideas of C++: **namespaces** and **scope resolution**.

Is this new to you? Read **LESSON.md** first, or press **Lesson** in the app.

## Your tasks

1. **Calculator namespace**: write `Calculator::add`, `subtract` and `multiply`. Each takes (int, int) and returns int.
2. **Scope resolution**: make 3 variables:
   - a global `int counter = 0`
   - `Game::counter = 10`
   - `Game::Player::counter = 100`

   Then write `int sumCounters()`. It returns the sum of all 3. Use `::` to reach each one.
3. **Nested namespaces**: write `Organization::HR::Payroll::calculateSalary(double base, double bonus)`. Declare it with the C++17 nested syntax.
4. **Aliases and using**: write these:
   - `DataProcessing::Statistics::average` and `maximum`. Both take (const std::vector<int>&).
   - `DataProcessing::Formatters::formatResult(label, double)`. It returns `"label: value"`. Use `std::to_string` for the value.
5. **Geometry**: write `Geometry::circleArea(r)` and `Geometry::rectangleArea(l, w)`.
6. **Banking**: write the class `Banking::Account(int number, double balance)`. It has:
   - `deposit`
   - `withdraw` (it returns false if there is not enough money)
   - `balance()`

   Also write a free function (a function that is not in a class): `Banking::transferFunds(Account& from, Account& to, double amount)`. It returns bool.
7. **Deep hierarchy**: write these:
   - `Company::Division::Department::Team::Resources::Employee(name)`. Its `getInfo()` returns `"Employee: <name>"`.
   - `Company::Division::Finance::Accounting::calculateBudget(double perHead, int heads)`.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
