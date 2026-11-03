// C++ Toolbox 3: references.
#pragma once
#include <vector>

int plusOne(int x) {
    return x + 1;
}

void addOne(int& x) {
    x = x + 1;
}

void swapValues(int& a, int& b) {
    int old = a;
    a = b;
    b = old;
}

void doubleAll(std::vector<int>& v) {
    for (int& x : v) x = x * 2;
}

int total(const std::vector<int>& v) {
    int sum = 0;
    for (int x : v) sum += x;
    return sum;
}
