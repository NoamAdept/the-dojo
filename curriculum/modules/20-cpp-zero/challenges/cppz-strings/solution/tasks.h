// C++ Toolbox 1: text with std::string.
#pragma once
#include <string>

std::string makeGreeting(std::string name) {
    return "Hello, " + name + "!";
}

int countChar(std::string text, char c) {
    int count = 0;
    for (std::size_t i = 0; i < text.size(); i++) {
        if (text[i] == c) count++;
    }
    return count;
}

bool isYes(std::string answer) {
    return answer == "yes" || answer == "y";
}

std::string keyOf(std::string line) {
    std::size_t pos = line.find('=');
    if (pos == std::string::npos) return line;
    return line.substr(0, pos);
}

std::string valueOf(std::string line) {
    std::size_t pos = line.find('=');
    if (pos == std::string::npos) return "";
    return line.substr(pos + 1);
}
