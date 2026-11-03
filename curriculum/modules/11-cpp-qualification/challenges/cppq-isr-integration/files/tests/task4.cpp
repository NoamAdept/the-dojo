// Task 4: debounce
#include "check.h"
#include "tasks.h"
int main() {
    resetDebounce();
    EXPECT(EXTI_ISR(100) && !EXTI_ISR(110) && EXTI_ISR(200) && !EXTI_ISR(249) && EXTI_ISR(250));
    resetDebounce();
    EXPECT(EXTI_ISR(0));
}
