// Task 6: config map dump
#include "check.h"
#include "tasks.h"
int main() {
    std::map<std::string, ConfigValue> cfg{{"mode", std::string("fm")}, {"gain", 30}, {"bw", 0.5f}};
    EXPECT(dumpConfig(cfg) == "bw=float:0.5;gain=int:30;mode=string:fm");
}
