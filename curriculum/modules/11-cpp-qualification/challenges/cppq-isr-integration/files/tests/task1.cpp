// Task 1: extern "C" handler
#include "check.h"
#include "tasks.h"
// Re-declaring with C linkage fails to compile if tasks.h declared it with C++ linkage.
extern "C" void ADC_IRQHandler();
int main() {
    ADC_IRQHandler();
    ADC_IRQHandler();
    EXPECT(g_adcIrqCount == 2);
}
