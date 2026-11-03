// Task 2: move ownership into a function
#include <type_traits>
#include "check.h"
#include "tasks.h"
int main() {
    auto ptr = std::make_unique<int>(50);
    EXPECT(takeOwnership(std::move(ptr)) == 50);
    EXPECT(ptr == nullptr);
}
