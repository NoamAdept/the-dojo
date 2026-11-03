// Task 4: writeLines
#include <cstdio>
#include <sstream>
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    bool ok = writeLines("tmp_task4.txt", {"gain=30", "rate=2400", "mode=fm"});
    std::stringstream got;
    { std::ifstream f("tmp_task4.txt"); got << f.rdbuf(); }
    std::remove("tmp_task4.txt");
    SAY(ok, "writeLines should return true when it could write the file");
    SAY(got.str() == "gain=30\nrate=2400\nmode=fm\n", "the written file should be \"gain=30\\nrate=2400\\nmode=fm\\n\" but was " << shown(got.str()));
    SAY(!writeLines("no_such_folder/out.txt", {"x"}), "writeLines into a folder that does not exist should return false. Check if (!out) after opening.");
}
