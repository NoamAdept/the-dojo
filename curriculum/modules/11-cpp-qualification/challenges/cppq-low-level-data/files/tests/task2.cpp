// Task 2: generic toggleBit
#include "check.h"
#include "tasks.h"
int main() {
    EXPECT(toggleBit<uint8_t>(0b1010, 0) == 0b1011);
    EXPECT(toggleBit<uint8_t>(0b1011, 3) == 0b0011);
    EXPECT(toggleBit<uint32_t>(0, 31) == 0x80000000u);
}
