// Task 1: RGB pack/unpack
#include "check.h"
#include "tasks.h"
int main() {
    EXPECT(packRGB(0x12, 0x34, 0x56) == 0x00123456u);
    EXPECT(packRGB(255, 255, 255) == 0x00FFFFFFu);
    uint8_t r, g, b;
    unpackRGB(0x00ABCDEFu, r, g, b);
    EXPECT(r == 0xAB && g == 0xCD && b == 0xEF);
}
