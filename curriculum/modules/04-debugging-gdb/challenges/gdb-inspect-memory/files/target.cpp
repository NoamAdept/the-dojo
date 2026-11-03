#include <cstdint>
#include <iostream>

static void inspect_packet(const std::uint8_t *packet) {
    std::cout << int(packet[0]) << '\n';
}

int main() {
    std::uint8_t packet[8] = {0xaa, 0x55, 0x03, 0x10, 0x00, 0xfe, 0x01, 0xef};
    inspect_packet(packet);
    return 0;
}
