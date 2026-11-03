// Task 4: mock vcpkg install
#include "check.h"
#include "tasks.h"
int main() {
    auto lines = mockInstall("fmt");
    EXPECT(lines.size() == 2 && lines[0] == "Computing installation plan..." && lines[1] == "Done installing: fmt");
}
