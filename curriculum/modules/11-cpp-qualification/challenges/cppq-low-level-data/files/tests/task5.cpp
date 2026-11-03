// Task 5: read header through reinterpret_cast
#include "check.h"
#include "tasks.h"
static_assert(sizeof(PacketHeader) == 3, "PacketHeader must be packed to 3 bytes");
int main() {
    const uint8_t raw[] = {0x01, 0x00, 0x05, 0x48, 0x45, 0x4C, 0x4C, 0x4F};
    PacketHeader h = readHeader(raw);
    EXPECT(h.id == 1 && h.len == 5);
}
