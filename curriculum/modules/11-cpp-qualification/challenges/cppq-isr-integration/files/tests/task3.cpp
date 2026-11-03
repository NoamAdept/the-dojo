// Task 3: static member as ISR target
#include "check.h"
#include "tasks.h"
int main() {
    void (*isr)() = &Motor::emergencyStop;  // static methods convert to plain function pointers
    EXPECT(isr != nullptr && !Motor::stopped);
    Button_ISR();
    EXPECT(Motor::stopped);
}
