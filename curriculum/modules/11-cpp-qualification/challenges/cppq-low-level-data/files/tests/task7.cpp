// Task 7: sensor variant with std::visit
#include "check.h"
#include "tasks.h"
int main() {
    EXPECT(formatSensor(SensorValue{12}) == "count=12");
    EXPECT(formatSensor(SensorValue{3.3}) == "volts=3.30");
    EXPECT(formatSensor(SensorValue{std::string("overrange")}) == "error: overrange");
}
