# Config That Lasts

`cppq-strings-files` · Orange Belt

**Goal:** Write seven small string and file helpers in `tasks.h`: formatting, `stoi`, writing and reading text files, a CSV parser and a line/word/character counter.

**File `tasks.h`**

```cpp
#pragma once
#include <fstream>
#include <sstream>
#include <string>

inline std::string bondName(const std::string& first, const std::string& last) {
    return last + ", " + first + " " + last + ".";
}

inline int addFifty(const std::string& s) { return std::stoi(s) + 50; }

inline bool writeLog(const std::string& path, const std::string& message) {
    std::ofstream out(path);
    if (!out.is_open()) return false;
    out << message << "\n";
    return true;
}

inline std::string readFirstLine(const std::string& path) {
    std::ifstream in(path);
    std::string line;
    if (in) std::getline(in, line);
    return line;
}

inline void saveProfile(const std::string& path, const std::string& name, int age) {
    std::ofstream(path) << "Name: " << name << ", Age: " << age << "\n";
}

inline bool verifyProfile(const std::string& path, const std::string& name, int age) {
    return readFirstLine(path) == "Name: " + name + ", Age: " + std::to_string(age);
}

struct Product {
    std::string name;
    double price;
    int quantity;
};

inline Product parseProduct(const std::string& csv) {
    std::size_t a = csv.find(','), b = csv.find(',', a + 1);
    return {csv.substr(0, a), std::stod(csv.substr(a + 1, b - a - 1)), std::stoi(csv.substr(b + 1))};
}

inline double totalValue(const Product& p) { return p.price * p.quantity; }

struct TextStats {
    int lines;
    int words;
    int characters;
};

inline TextStats fileStats(const std::string& path) {
    TextStats s{0, 0, 0};
    std::ifstream in(path);
    std::string line, word;
    while (std::getline(in, line)) {
        ++s.lines;
        s.characters += static_cast<int>(line.size());
        std::istringstream words(line);
        while (words >> word) ++s.words;
    }
    return s;
}
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
