#pragma once
#include <cstddef>
#include <cstdint>

// The header as the program keeps it in memory (not how the bytes arrive).
struct header {
    char tag[2];        // two ASCII letters, like 'R' 'X'
    uint16_t sequence;  // message counter
    uint8_t flags;      // 8 on/off bits
    uint8_t length;     // payload length in bytes
};

// Fills *out from the first 6 bytes of data and returns true.
// Returns false, without reading any byte, when the input is bad.
bool decode_header(const uint8_t* data, std::size_t size, header* out);
