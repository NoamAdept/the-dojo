// C++ Toolbox 6: lookups with std::map and auto.
#pragma once
#include <map>
#include <string>
#include <vector>

std::map<std::string, int> countWords(const std::vector<std::string>& words) {
    std::map<std::string, int> counts;
    for (const auto& w : words) counts[w]++;
    return counts;
}

int lookup(const std::map<std::string, int>& m, const std::string& key) {
    if (m.count(key) == 0) return -1;
    return m.at(key);
}

int totalOfValues(const std::map<std::string, int>& m) {
    int total = 0;
    for (const auto& entry : m) total += entry.second;
    return total;
}

std::string describe(const std::map<std::string, int>& m) {
    std::string out;
    for (const auto& entry : m) {
        out += entry.first + "=" + std::to_string(entry.second) + ";";
    }
    return out;
}

std::string mostCommon(const std::vector<std::string>& words) {
    std::string best;
    int bestCount = 0;
    for (const auto& entry : countWords(words)) {
        if (entry.second > bestCount) {  // strict >, so the first (alphabetical) word wins ties
            best = entry.first;
            bestCount = entry.second;
        }
    }
    return best;
}
