// Task 5: myMax
#include "check.h"
#include "tasks.h"
int main() {
    EXPECT(myMax(3, 9) == 9 && myMax(2.5, -1.0) == 2.5);
    EXPECT(myMax(std::string("apple"), std::string("banana")) == "banana");
}
