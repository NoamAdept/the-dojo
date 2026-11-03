// C++ Qualification 13: templates and generic programming.
#pragma once
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

template <class T>
void mySwap(T& a, T& b) {
    T tmp = std::move(a);
    a = std::move(b);
    b = std::move(tmp);
}

template <class T>
T add(T a, T b) {
    return a + b;
}

template <class T>
class Holder {
public:
    explicit Holder(T content) : content_(std::move(content)) {}
    const T& get() const { return content_; }
    std::string display() const {
        std::ostringstream out;
        out << content_;
        return out.str();
    }

private:
    T content_;
};

template <class A, class B, class C>
std::string printTriplet(A a, B b, C c) {
    std::ostringstream out;
    out << "(" << a << ", " << b << ", " << c << ")";
    return out.str();
}

template <class T>
const T& myMax(const T& a, const T& b) {
    return a > b ? a : b;
}

template <class K, class V>
struct MyPair {
    K key;
    V value;
    MyPair(K k, V v) : key(std::move(k)), value(std::move(v)) {}
    std::string print() const {
        std::ostringstream out;
        out << "Key: " << key << ", Value: " << value;
        return out.str();
    }
};

template <class T>
class Stack {
public:
    void push(T val) { items_.push_back(std::move(val)); }
    void pop() {
        if (items_.empty()) throw std::out_of_range("pop on empty stack");
        items_.pop_back();
    }
    const T& top() const {
        if (items_.empty()) throw std::out_of_range("top on empty stack");
        return items_.back();
    }
    bool isEmpty() const { return items_.empty(); }

private:
    std::vector<T> items_;
};
