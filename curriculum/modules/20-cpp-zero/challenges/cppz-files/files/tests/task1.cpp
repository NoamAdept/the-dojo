// Task 1: countLines
#include <cstdio>
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    { std::ofstream f("tmp_task1.txt"); f << "alpha\nbravo\n\ncharlie\ndelta\n"; }
    int n = countLines("tmp_task1.txt");
    std::remove("tmp_task1.txt");
    SAY(n == 5, "a file with 5 lines (one of them empty) should give countLines 5, but gave " << n);
    n = countLines("no_such_folder/missing.txt");
    SAY(n == -1, "countLines on a file that does not exist should be -1, but was " << n << ". Check if (!in) after opening.");
}
