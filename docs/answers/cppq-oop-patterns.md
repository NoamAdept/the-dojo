# OOP and Design Patterns

`cppq-oop-patterns` · Orange Belt

**Goal:** Write a small class with an invariant, a Singleton logger, an abstract `Shape` with a factory, and an Observer setup (`Sensor`, `Display`, `Alarm`) in `tasks.h`.

**File `tasks.h`**

```cpp
#pragma once
#include <iostream>
#include <memory>
#include <string>
#include <vector>

class Dog {
public:
    void setAge(int age) {
        if (age >= 0 && age <= 30) age_ = age;
    }
    int age() const { return age_; }
    std::string bark() const { return "Woof!"; }

private:
    int age_ = 0;
};

class Logger {
public:
    static Logger& instance() {
        static Logger logger;
        return logger;
    }
    Logger(const Logger&) = delete;
    Logger& operator=(const Logger&) = delete;
    void log(const std::string& msg) { messages_.push_back(msg); }
    int count() const { return static_cast<int>(messages_.size()); }

private:
    Logger() = default;
    std::vector<std::string> messages_;
};

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

class Shape {
public:
    virtual ~Shape() = default;
    virtual std::string draw() const = 0;
};

class Circle : public Shape {
public:
    std::string draw() const override { return "circle"; }
};

class Square : public Shape {
public:
    std::string draw() const override { return "square"; }
};

inline std::unique_ptr<Shape> makeShape(const std::string& kind) {
    if (kind == "circle") return std::make_unique<Circle>();
    if (kind == "square") return std::make_unique<Square>();
    return nullptr;
}

class Observer {
public:
    virtual ~Observer() = default;
    virtual void update(int value) = 0;
};

class Sensor {
public:
    void attach(Observer* o) { observers_.push_back(o); }
    void notify(int value) {
        for (Observer* o : observers_) o->update(value);
    }

private:
    std::vector<Observer*> observers_;
};

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

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
