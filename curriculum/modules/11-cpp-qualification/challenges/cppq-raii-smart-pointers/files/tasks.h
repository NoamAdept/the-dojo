// C++ Qualification 08: RAII and smart pointers.
#pragma once
#include <memory>
#include <string>
#include <vector>

inline std::vector<std::string> g_events;  // destructors record what happened here

// Task 1: class Widget; std::unique_ptr<Widget> makeWidget()
// Task 2: int takeOwnership(std::unique_ptr<int> p)
// Task 3: long sharedCountDemo()
// Task 4: class ScopeLogger
// Task 5: std::unique_ptr<int> createObject(int value)
// Task 6: struct Node; makeChain(...); traverse(...)
// Task 7: class FileManager
