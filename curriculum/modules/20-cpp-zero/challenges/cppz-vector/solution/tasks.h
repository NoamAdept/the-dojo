// C++ Toolbox 2: lists with std::vector.
#pragma once
#include <string>
#include <vector>

int sumAll(std::vector<int> v) {
    int total = 0;
    for (int x : v) total += x;
    return total;
}

int countAbove(std::vector<int> v, int limit) {
    int count = 0;
    for (int x : v) {
        if (x > limit) count++;
    }
    return count;
}

std::vector<int> makeRange(int n) {
    std::vector<int> out;
    for (int i = 1; i <= n; i++) out.push_back(i);
    return out;
}

int largest(std::vector<int> v) {
    int best = v[0];
    for (int x : v) {
        if (x > best) best = x;
    }
    return best;
}

std::vector<std::string> longWords(std::vector<std::string> words, std::size_t minLen) {
    std::vector<std::string> out;
    for (std::string w : words) {
        if (w.size() >= minLen) out.push_back(w);
    }
    return out;
}
