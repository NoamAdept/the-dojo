// Task 6: manifest dependency parser
#include "check.h"
#include "tasks.h"
int main() {
    EXPECT((parseDependencies(R"({"name": "x", "dependencies": ["fmt", "zlib"]})") == std::vector<std::string>{"fmt", "zlib"}));
    EXPECT((parseDependencies(R"({"dependencies":[ "a" ,"b-c"], "version": "1"})") == std::vector<std::string>{"a", "b-c"}));
    EXPECT(parseDependencies(R"({"dependencies": []})").empty());
    EXPECT(parseDependencies(R"({"name": "none"})").empty());
}
