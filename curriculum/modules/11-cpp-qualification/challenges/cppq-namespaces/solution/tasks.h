// C++ Qualification 01: namespaces and scope resolution.
#pragma once
#include <algorithm>
#include <cmath>
#include <string>
#include <vector>

namespace Calculator {
inline int add(int a, int b) { return a + b; }
inline int subtract(int a, int b) { return a - b; }
inline int multiply(int a, int b) { return a * b; }
}  // namespace Calculator

inline int counter = 0;
namespace Game {
inline int counter = 10;
namespace Player {
inline int counter = 100;
}
}  // namespace Game
inline int sumCounters() { return ::counter + Game::counter + Game::Player::counter; }

namespace Organization::HR::Payroll {
inline double calculateSalary(double base, double bonus) { return base + bonus; }
}

namespace DataProcessing {
namespace Statistics {
inline double average(const std::vector<int>& data) {
    if (data.empty()) return 0.0;
    double sum = 0.0;
    for (int v : data) sum += v;
    return sum / data.size();
}
inline int maximum(const std::vector<int>& data) { return *std::max_element(data.begin(), data.end()); }
}  // namespace Statistics
namespace Formatters {
inline std::string formatResult(const std::string& label, double value) {
    return label + ": " + std::to_string(value);
}
}  // namespace Formatters
}  // namespace DataProcessing

namespace Geometry {
inline double circleArea(double r) { return M_PI * r * r; }
inline double rectangleArea(double l, double w) { return l * w; }
}  // namespace Geometry

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
    int number() const { return number_; }

private:
    int number_;
    double balance_;
};
inline bool transferFunds(Account& from, Account& to, double amount) {
    if (!from.withdraw(amount)) return false;
    to.deposit(amount);
    return true;
}
}  // namespace Banking

namespace Company::Division::Department::Team::Resources {
class Employee {
public:
    explicit Employee(std::string name) : name_(std::move(name)) {}
    std::string getInfo() const { return "Employee: " + name_; }

private:
    std::string name_;
};
}  // namespace Company::Division::Department::Team::Resources

namespace Company::Division::Finance::Accounting {
inline double calculateBudget(double perHead, int heads) { return perHead * heads; }
}
