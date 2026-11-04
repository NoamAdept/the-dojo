# RAII and Smart Pointers

`cppq-raii-smart-pointers` · Orange Belt

**Goal:** Write classes whose constructors and destructors log to a global `g_events` list, and functions that create, move and share `unique_ptr` / `shared_ptr` objects, including a `unique_ptr` linked list.

**File `tasks.h`**

```cpp
#pragma once
#include <memory>
#include <string>
#include <vector>

inline std::vector<std::string> g_events;

class Widget {
public:
    Widget() { g_events.push_back("built"); }
    ~Widget() { g_events.push_back("broken"); }
    void spin() {}
};

inline std::unique_ptr<Widget> makeWidget() { return std::make_unique<Widget>(); }

inline int takeOwnership(std::unique_ptr<int> p) { return *p; }

inline long sharedCountDemo() {
    auto p1 = std::make_shared<int>(100);
    long inside = 0;
    {
        auto p2 = p1;
        inside = p1.use_count();
    }
    return inside;
}

class ScopeLogger {
public:
    explicit ScopeLogger(std::string name) : name_(std::move(name)) { g_events.push_back("Enter: " + name_); }
    ~ScopeLogger() { g_events.push_back("Exit: " + name_); }

private:
    std::string name_;
};

inline std::unique_ptr<int> createObject(int value) { return std::make_unique<int>(value); }

struct Node {
    int data;
    std::unique_ptr<Node> next;
};

inline std::unique_ptr<Node> makeChain(const std::vector<int>& values) {
    std::unique_ptr<Node> head;
    for (auto it = values.rbegin(); it != values.rend(); ++it)
        head = std::make_unique<Node>(Node{*it, std::move(head)});
    return head;
}

inline std::vector<int> traverse(const Node* node) {
    std::vector<int> out;
    for (; node; node = node->next.get()) out.push_back(node->data);
    return out;
}

class FileManager {
public:
    explicit FileManager(std::string name) : name_(std::move(name)) { g_events.push_back("Opening " + name_); }
    ~FileManager() { g_events.push_back("Closing " + name_); }
    void write(const std::string& msg) { g_events.push_back(msg); }

private:
    std::string name_;
};
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
