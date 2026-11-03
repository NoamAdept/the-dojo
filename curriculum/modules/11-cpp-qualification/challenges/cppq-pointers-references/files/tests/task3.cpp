// Task 3: walk a C string with a pointer
#include <fstream>
#include <iterator>
#include "check.h"
#include "tasks.h"
int main() {
    EXPECT(walkCString("Hello") == "Hello");
    EXPECT(walkCString("") == "");
    std::ifstream f("tasks.h");
    std::string src((std::istreambuf_iterator<char>(f)), {});
    EXPECT(!contains(src, "strlen("));
}
