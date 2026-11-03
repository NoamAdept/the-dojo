// Task 3: Holder<T>
#include "check.h"
#include "tasks.h"
int main() {
    Holder<int> h(42);
    Holder<std::string> s("rx");
    EXPECT(h.get() == 42 && h.display() == "42" && s.display() == "rx");
}
