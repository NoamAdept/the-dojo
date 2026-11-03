// Task 2: readLines
#include <cstdio>
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    { std::ofstream f("tmp_task2.txt"); f << "first line\nsecond\nthird one\n"; }
    std::vector<std::string> lines = readLines("tmp_task2.txt");
    std::remove("tmp_task2.txt");
    SAY(lines.size() == 3, "the test file has 3 lines but readLines returned " << lines.size());
    SAY(lines[0] == "first line" && lines[2] == "third one", "readLines should return the lines in order without the \\n, but line 1 was " << shown(lines[0]));
    SAY(readLines("no_such_folder/missing.txt").empty(), "readLines on a missing file should return an empty vector");
}
