// Task 6: unique_ptr linked list
#include "check.h"
#include "tasks.h"
int main() {
    auto head = makeChain({1, 2, 3});
    EXPECT((traverse(head.get()) == std::vector<int>{1, 2, 3}));
    EXPECT(traverse(nullptr).empty() && makeChain({}) == nullptr);
}
