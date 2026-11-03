// Task 5: profile saver
#include <cstdio>
#include "check.h"
#include "tasks.h"
int main() {
    saveProfile("t5.txt", "John", 30);
    EXPECT(readFirstLine("t5.txt") == "Name: John, Age: 30");
    EXPECT(verifyProfile("t5.txt", "John", 30));
    EXPECT(!verifyProfile("t5.txt", "John", 31));
    std::remove("t5.txt");
}
