// Tiny test helpers shared by the tests in this folder.
#pragma once
#include <iostream>
#include <sstream>
#include <string>

#define EXPECT(cond)                                                              \
    do {                                                                          \
        if (!(cond)) {                                                            \
            std::cerr << "expected: " #cond " (" __FILE__ ":" << __LINE__ << ")\n"; \
            return 1;                                                             \
        }                                                                         \
    } while (0)

// Captures everything written to std::cout while it is alive.
struct CaptureCout {
    std::ostringstream buf;
    std::streambuf* old;
    CaptureCout() : old(std::cout.rdbuf(buf.rdbuf())) {}
    ~CaptureCout() { std::cout.rdbuf(old); }
    std::string str() const { return buf.str(); }
};

inline bool contains(const std::string& hay, const std::string& needle) {
    return hay.find(needle) != std::string::npos;
}
