// C++ Toolbox 7: reading and writing text files.
#pragma once
#include <fstream>
#include <string>
#include <vector>

int countLines(const std::string& path) {
    std::ifstream in(path);
    if (!in) return -1;
    int count = 0;
    std::string line;
    while (std::getline(in, line)) count++;
    return count;
}

std::vector<std::string> readLines(const std::string& path) {
    std::vector<std::string> lines;
    std::ifstream in(path);
    std::string line;
    while (std::getline(in, line)) lines.push_back(line);  // a stream that failed to open reads nothing
    return lines;
}

int sumNumbers(const std::string& path) {
    int total = 0;
    for (const auto& line : readLines(path)) {
        if (!line.empty()) total += std::stoi(line);
    }
    return total;
}

bool writeLines(const std::string& path, const std::vector<std::string>& lines) {
    std::ofstream out(path);
    if (!out) return false;
    for (const auto& line : lines) out << line << "\n";
    return true;
}

std::string findSetting(const std::string& path, const std::string& key) {
    for (const auto& line : readLines(path)) {
        std::size_t pos = line.find('=');
        if (pos != std::string::npos && line.substr(0, pos) == key) {
            return line.substr(pos + 1);
        }
    }
    return "";
}
