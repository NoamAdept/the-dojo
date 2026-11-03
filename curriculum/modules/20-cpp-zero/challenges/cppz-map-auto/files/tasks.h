// C++ Toolbox 6: lookups with std::map and auto.
#pragma once
#include <map>
#include <string>
#include <vector>

// Task 1: map each word to how many times it appears.
std::map<std::string, int> countWords(const std::vector<std::string>& words) {
    std::map<std::string, int> counts;
    return counts;  // fill counts before returning it
}

// Task 2: the value for key, or -1 if key is not in m.
int lookup(const std::map<std::string, int>& m, const std::string& key) {
    return -2;  // replace this line
}

// Task 3: the sum of all values in m.
int totalOfValues(const std::map<std::string, int>& m) {
    return -1;  // replace this line
}

// Task 4: "key=value;" for every pair, in order. Example: "am=1;fm=2;"
std::string describe(const std::map<std::string, int>& m) {
    return "?";  // replace this line
}

// Task 5: the most common word (ties: the alphabetically first one).
std::string mostCommon(const std::vector<std::string>& words) {
    return "";  // replace this line
}
