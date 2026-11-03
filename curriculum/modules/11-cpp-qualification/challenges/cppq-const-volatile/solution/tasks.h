// C++ Qualification 04: const and volatile qualifiers.
#pragma once
#include <chrono>
#include <iostream>
#include <map>
#include <string>
#include <thread>

using ConstPtrToInt = int* const;
inline int* const makeConstPtr(int& x) { return &x; }

struct MyData {
    int val;
};
inline int printData(const MyData& d) { return d.val; }

class Calculator {
public:
    int heavyCalc() const {
        if (cache_ == -1) {
            cache_ = 42;
            ++computations_;
        }
        return cache_;
    }
    int computations() const { return computations_; }

private:
    mutable int cache_ = -1;
    mutable int computations_ = 0;
};

constexpr int square(int x) { return x * x; }
constexpr int kArraySize = square(5);

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

class PrimeChecker {
public:
    bool isPrime(int n) const {
        auto it = cache_.find(n);
        if (it != cache_.end()) return it->second;
        std::cout << "Calculating " << n << "\n";
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

inline void hardwareWrite(volatile int* reg, int pattern, int delayMs) {
    std::this_thread::sleep_for(std::chrono::milliseconds(delayMs));
    *reg = pattern;
}

// ponytail: volatile works here because x86/ARM int stores are atomic in practice;
// real cross-thread code should use std::atomic<int> instead.
inline int waitForSignal(volatile int* reg, int pattern) {
    while (*reg != pattern) {
    }
    std::cout << "Hardware signal received!\n";
    return *reg;
}
