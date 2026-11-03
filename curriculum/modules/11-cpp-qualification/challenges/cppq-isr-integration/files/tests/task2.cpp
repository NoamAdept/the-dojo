// Task 2: volatile flag set by ISR
#include <type_traits>
#include "check.h"
#include "tasks.h"
int main() {
    static_assert(std::is_volatile_v<std::remove_reference_t<decltype(conversionDone)>>, "make it volatile");
    EXPECT(!conversionDone);
    ADC_ISR();
    EXPECT(conversionDone);
}
