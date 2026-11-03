// Task 7: Stack<T>
#include "check.h"
#include "tasks.h"
int main() {
    Stack<int> s;
    EXPECT(s.isEmpty());
    s.push(1);
    s.push(2);
    EXPECT(s.top() == 2);
    s.pop();
    EXPECT(s.top() == 1);
    s.pop();
    bool threw = false;
    try { s.top(); } catch (const std::out_of_range&) { threw = true; }
    EXPECT(threw && s.isEmpty());
    Stack<std::string> words;
    words.push("hi");
    EXPECT(words.top() == "hi");
}
