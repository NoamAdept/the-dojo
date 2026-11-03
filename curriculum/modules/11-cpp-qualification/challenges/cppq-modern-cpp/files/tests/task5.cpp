// Task 5: std::variant + std::visit
#include "check.h"
#include "tasks.h"
int main() {
    EXPECT(describe(ConfigValue{3}) == "int:3");
    EXPECT(describe(ConfigValue{2.5f}) == "float:2.5");
    EXPECT(describe(ConfigValue{std::string("fm")}) == "string:fm");
}
