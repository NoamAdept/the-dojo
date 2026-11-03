// C++ Qualification 07: STL containers, algorithms and iterators.
#pragma once
#include <algorithm>
#include <functional>
#include <map>
#include <numeric>
#include <set>
#include <sstream>
#include <string>
#include <vector>

inline float middleElement(const std::vector<float>& v) { return v[v.size() / 2]; }

inline std::string lookup(const std::map<std::string, std::string>& book, const std::string& name) {
    auto it = book.find(name);
    return it == book.end() ? "not found" : it->second;
}

inline std::size_t uniqueCount(const std::vector<std::string>& words) {
    return std::set<std::string>(words.begin(), words.end()).size();
}

inline std::vector<int> sortedDescending(std::vector<int> v) {
    std::sort(v.begin(), v.end(), std::greater<int>());
    return v;
}

struct GradeReport {
    double average;
    int max;
    int count;
};

inline GradeReport analyzeGrades(const std::vector<int>& input) {
    std::vector<int> grades;
    for (int g : input) {
        if (g == -1) break;
        grades.push_back(g);
    }
    if (grades.empty()) return {0.0, 0, 0};
    double avg = std::accumulate(grades.begin(), grades.end(), 0.0) / grades.size();
    return {avg, *std::max_element(grades.begin(), grades.end()), static_cast<int>(grades.size())};
}

inline std::map<std::string, int> wordFrequency(const std::string& text) {
    std::map<std::string, int> counts;
    std::istringstream in(text);
    std::string word;
    while (in >> word) ++counts[word];
    return counts;
}

struct Player {
    std::string name;
    int score;
};

inline void rankPlayers(std::vector<Player>& players) {
    std::sort(players.begin(), players.end(), [](const Player& a, const Player& b) {
        if (a.score != b.score) return a.score > b.score;
        return a.name < b.name;
    });
}
