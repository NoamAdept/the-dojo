// C++ Qualification 12: low-level data manipulation.
#pragma once
#include <cstdint>
#include <cstdio>
#include <string>
#include <type_traits>
#include <variant>

inline uint32_t packRGB(uint8_t r, uint8_t g, uint8_t b) {
    return (uint32_t(r) << 16) | (uint32_t(g) << 8) | uint32_t(b);
}

inline void unpackRGB(uint32_t c, uint8_t& r, uint8_t& g, uint8_t& b) {
    r = (c >> 16) & 0xFF;
    g = (c >> 8) & 0xFF;
    b = c & 0xFF;
}

template <class T>
T toggleBit(T val, unsigned n) {
    return static_cast<T>(val ^ (T(1) << n));
}

#pragma pack(push, 1)
struct Header {
    uint16_t id;
    uint8_t flags;
    uint8_t len;
};
struct PacketHeader {
    uint16_t id;
    uint8_t len;
};
#pragma pack(pop)
static_assert(sizeof(Header) == 4);

inline bool isPowerOfTwo(int n) { return n > 0 && (n & (n - 1)) == 0; }

// ponytail: reinterpret_cast on a packed struct assumes a little-endian host (Pi, x86).
inline PacketHeader readHeader(const uint8_t* raw) { return *reinterpret_cast<const PacketHeader*>(raw); }

inline std::string readPayload(const uint8_t* raw) {
    const PacketHeader* h = reinterpret_cast<const PacketHeader*>(raw);
    const char* data = reinterpret_cast<const char*>(raw + sizeof(PacketHeader));
    return std::string(data, data + h->len);
}

using SensorValue = std::variant<int, double, std::string>;

inline std::string formatSensor(const SensorValue& v) {
    return std::visit(
        [](const auto& x) -> std::string {
            using T = std::decay_t<decltype(x)>;
            if constexpr (std::is_same_v<T, int>) {
                return "count=" + std::to_string(x);
            } else if constexpr (std::is_same_v<T, double>) {
                char buf[32];
                std::snprintf(buf, sizeof buf, "volts=%.2f", x);
                return buf;
            } else {
                return "error: " + x;
            }
        },
        v);
}
