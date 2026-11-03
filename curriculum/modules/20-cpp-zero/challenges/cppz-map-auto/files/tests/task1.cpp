// Task 1: countWords
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    auto m = countWords({"lora", "ads-b", "lora", "fm", "lora", "fm"});
    SAY(m.size() == 3, "countWords({\"lora\", \"ads-b\", \"lora\", \"fm\", \"lora\", \"fm\"}) should have 3 different words but has " << m.size());
    SAY(m.count("lora") && m.at("lora") == 3, "\"lora\" appears 3 times, but your map does not say 3");
    SAY(m.count("fm") && m.at("fm") == 2, "\"fm\" appears 2 times, but your map does not say 2");
    SAY(m.count("ads-b") && m.at("ads-b") == 1, "\"ads-b\" appears once, but your map does not say 1");
    SAY(countWords({}).empty(), "countWords of an empty list should give an empty map");
}
