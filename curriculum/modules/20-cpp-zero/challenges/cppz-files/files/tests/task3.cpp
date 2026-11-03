// Task 3: sumNumbers
#include <cstdio>
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    { std::ofstream f("tmp_task3.txt"); f << "120\n-20\n\n7\n1000\n"; }
    int s = sumNumbers("tmp_task3.txt");
    std::remove("tmp_task3.txt");
    SAY(s == 1107, "the numbers 120, -20, 7, 1000 (and one empty line) should sum to 1107, but sumNumbers gave " << s);
    s = sumNumbers("no_such_folder/missing.txt");
    SAY(s == 0, "sumNumbers on a missing file should be 0, but was " << s);
}
