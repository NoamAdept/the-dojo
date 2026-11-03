// Task 5: findSetting
#include <cstdio>
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    { std::ofstream f("tmp_task5.txt"); f << "device=rtl0\nfreq=144800000\ngain=33\nmode=nfm\n"; }
    std::string g = findSetting("tmp_task5.txt", "gain");
    std::string m = findSetting("tmp_task5.txt", "mode");
    std::string x = findSetting("tmp_task5.txt", "squelch");
    std::string fr = findSetting("tmp_task5.txt", "fre");
    std::remove("tmp_task5.txt");
    SAY(g == "33", "findSetting(file, \"gain\") should be \"33\" but was " << shown(g));
    SAY(m == "nfm", "findSetting(file, \"mode\") should be \"nfm\" (the last line) but was " << shown(m));
    SAY(x == "", "findSetting(file, \"squelch\") should be \"\" because no line has that key, but was " << shown(x));
    SAY(fr == "", "findSetting(file, \"fre\") should be \"\": the key must match the whole text before '=', not just the start of \"freq\". It was " << shown(fr));
    SAY(findSetting("no_such_folder/missing.txt", "gain") == "", "findSetting on a missing file should be \"\"");
}
