# OOP and Design Patterns: lesson

### What is a Class?

Think of a **Class** as a **blueprint** (a plan) or a template.
- It is a logical structure. It is a description, not a real thing in memory.
- It says what data an object holds and what the object can do.

### What is an Object?

Think of an **Object** as an **instance** of that class. An instance is one real thing made from the plan.
- It is a physical entity. It exists in memory.

### 1. Defining a Basic Class

```cpp
class ClassName {
    // Member variables (data)
    // Member functions (behavior)
};
```

```cpp
#include <iostream>
#include <string>

class Car {
public:
    std::string brand;
    int year;
};

int main() {
    Car myCar;
    myCar.brand = "Toyota";
    myCar.year = 2022;
    std::cout << "Car: " << myCar.brand << ", Year: " << myCar.year << std::endl;
    return 0;
}
```

### 2. Access Specifiers: `public` vs `private`

- **`public`**: code outside the class can use it.
- **`private`**: only code inside the class can use it. This is the default for classes.

Use **Encapsulation** to protect data. This means you keep data private and give access only through functions (Getters/Setters).

```cpp
#include <iostream>

class Account {
private:
    double balance = 0;

public:
    void deposit(double amount) {
        if (amount > 0) balance += amount;
    }
    
    double getBalance() { return balance; }
};

int main() {
    Account a;
    // a.balance = 100; // Error: private
    a.deposit(100);
    std::cout << "Balance: " << a.getBalance() << std::endl;
    return 0;
}
```

### 3. Constructors and Destructors

- **Constructor** (`ClassName()`): C++ calls it when the object is created. It initializes (sets up) the object.
- **Destructor** (`~ClassName()`): C++ calls it when the object is destroyed. It cleans up.

```cpp
#include <iostream>

class Session {
public:
    Session() { std::cout << "Session Start" << std::endl; }
    ~Session() { std::cout << "Session End" << std::endl; }
};

int main() {
    {
        Session s;
    } // Destructor called here
    return 0;
}
```

### 4. The `this` Pointer

`this` points to the current object. It helps when 2 names are the same, for example a parameter and a member with the same name.

### 5. Design Patterns for Embedded

A design pattern is a standard solution to a common problem. Embedded code runs on small devices that control hardware. So in embedded code, we focus on patterns that manage hardware well.

#### A. Singleton (The Hardware Manager)

A Singleton makes sure a class has only **one instance**. This is perfect for hardware resources that exist only once each, like UART or SPI.

```cpp
#include <iostream>

class UART {
public:
    // Delete copy/assign to prevent duplicates
    UART(const UART&) = delete;
    void operator=(const UART&) = delete;

    static UART& getInstance() {
        static UART instance; // Lazy initialization, thread-safe in C++11
        return instance;
    }

    void send(const char* msg) {
        std::cout << "[UART Tx]: " << msg << std::endl;
    }

private:
    UART() { std::cout << "UART Hardware Initialized" << std::endl; }
};

int main() {
    UART::getInstance().send("Hello World");
    return 0;
}
```

#### B. Factory Pattern

A Factory creates objects for you. You do not need to name the exact class. This is useful when you support many sensor types behind one common interface.

```cpp
#include <iostream>
#include <memory>

struct Sensor {
    virtual void read() = 0;
    virtual ~Sensor() {}
};

struct TempSensor : Sensor {
    void read() override { std::cout << "Reading Temp..." << std::endl; }
};

struct PressureSensor : Sensor {
    void read() override { std::cout << "Reading Pressure..." << std::endl; }
};

class SensorFactory {
public:
    enum Type { TEMP, PRESSURE };
    static std::unique_ptr<Sensor> create(Type t) {
        if (t == TEMP) return std::make_unique<TempSensor>();
        return std::make_unique<PressureSensor>();
    }
};

int main() {
    auto s = SensorFactory::create(SensorFactory::TEMP);
    s->read();
    return 0;
}
```

---

## New words

- **class**: a plan that says what data an object holds and what it can do.
- **object (instance)**: one real thing in memory, made from a class.
- **encapsulation**: keeping data private and giving access only through functions.
- **constructor / destructor**: functions that run when an object is created / destroyed.
- **design pattern**: a standard solution to a common problem.
- **Singleton**: a class that can have only one instance.
- **Factory**: a function or class that creates objects for you.
- **interface**: a set of functions that many classes promise to provide.
