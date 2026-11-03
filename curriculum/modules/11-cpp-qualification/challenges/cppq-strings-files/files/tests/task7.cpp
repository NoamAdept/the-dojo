// Task 7: text statistics
#include <cstdio>
#include "check.h"
#include "tasks.h"
int main() {
    { std::ofstream("t7.txt") << "the quick brown\nfox  jumps\n\nover the lazy dog\n"; }
    TextStats s = fileStats("t7.txt");
    std::remove("t7.txt");
    EXPECT(s.lines == 4);
    EXPECT(s.words == 9);
    EXPECT(s.characters == 15 + 10 + 0 + 17);
}
