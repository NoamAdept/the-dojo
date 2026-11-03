// Task 5: custom exception
#include <type_traits>
#include "check.h"
#include "tasks.h"
int main() {
    static_assert(std::is_base_of_v<std::exception, SensorException>);
    EXPECT(readSensor(4) == 40);
    try {
        readSensor(-2);
        EXPECT(false && "readSensor(-2) should throw");
    } catch (const std::exception& e) {
        EXPECT(std::string(e.what()) == "sensor -2 failed");
    }
}
