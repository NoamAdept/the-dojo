// Task 6: payload via pointer arithmetic
#include "check.h"
#include "tasks.h"
int main() {
    const uint8_t raw[] = {0x01, 0x00, 0x05, 0x48, 0x45, 0x4C, 0x4C, 0x4F, 0x21};
    EXPECT(readPayload(raw) == "HELLO");
}
