#include <iomanip>
#include <iostream>
#include "structs.hpp"

void print_byte(uint8_t b)
{
    std::cout << "0x" << std::hex << std::setw(2) << std::setfill('0') << static_cast<int>(b) << std::dec << "\n";
}

std::size_t sample_bytes(std::size_t count)
{
    return count * sizeof(uint16_t);
}

reading make_reading(uint16_t channel, uint32_t freq_hz, uint8_t gain)
{
    reading r{};
    r.channel = channel;
    r.freq_hz = freq_hz;
    r.gain = gain;
    return r;
}

void retune(reading* r, uint32_t freq_hz)
{
    r->freq_hz = freq_hz;
}

uint8_t low_nibble(uint8_t b)
{
    return b & 0x0f;
}

uint8_t high_nibble(uint8_t b)
{
    return b >> 4;
}

bool bit_is_set(uint8_t flags, unsigned bit)
{
    return ((flags >> bit) & 1u) != 0;
}

uint16_t read_be16(const uint8_t* p)
{
    return static_cast<uint16_t>((p[0] << 8) | p[1]);
}

uint32_t read_le32(const uint8_t* p)
{
    return static_cast<uint32_t>(p[0]) | (static_cast<uint32_t>(p[1]) << 8)
         | (static_cast<uint32_t>(p[2]) << 16) | (static_cast<uint32_t>(p[3]) << 24);
}
