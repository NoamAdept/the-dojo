// C++ Toolbox 7: reading and writing text files.
#pragma once
#include <fstream>
#include <string>
#include <vector>

// Task 1: number of lines in the file, or -1 if it cannot be opened.
int countLines(const std::string& path) {
    return -2;  // replace this line
}

// Task 2: all lines of the file, in order (empty if it cannot be opened).
std::vector<std::string> readLines(const std::string& path) {
    std::vector<std::string> lines;
    return lines;  // fill lines before returning it
}

// Task 3: sum of the whole numbers in the file, one per line. Skip empty lines.
int sumNumbers(const std::string& path) {
    return -1;  // replace this line
}

// Task 4: write each string on its own line. false if the file cannot be created.
bool writeLines(const std::string& path, const std::vector<std::string>& lines) {
    return false;  // replace this line
}

// Task 5: for a line "key=value", return value. "" if the key is not in the file.
std::string findSetting(const std::string& path, const std::string& key) {
    return "?";  // replace this line
}
