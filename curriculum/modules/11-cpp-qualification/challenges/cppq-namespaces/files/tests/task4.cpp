// Task 4: aliases and using declarations
#include "check.h"
#include "tasks.h"
int main() {
    namespace stats = DataProcessing::Statistics;
    using DataProcessing::Formatters::formatResult;
    std::vector<int> v{10, 20, 30, 40, 50};
    EXPECT(stats::average(v) == 30.0);
    EXPECT(stats::average({}) == 0.0);
    EXPECT(stats::maximum(v) == 50);
    EXPECT(formatResult("Average", 30.0) == "Average: " + std::to_string(30.0));
}
