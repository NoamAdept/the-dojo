// Helpers that turn a failed test into a plain-English message.
#pragma once
#include <iostream>
#include <string>

// SAY(condition, message): if the condition is false, print the message and fail this task.
#define SAY(cond, msg)                      \
    do {                                    \
        if (!(cond)) {                      \
            std::cerr << msg << "\n";       \
            return 1;                       \
        }                                   \
    } while (0)

// Shows text in quotes, with line breaks written as \n so the message stays on one line.
inline std::string shown(const std::string& s) {
    std::string r = "\"";
    for (char c : s) {
        if (c == '\n') r += "\\n";
        else r += c;
    }
    return r + "\"";
}
