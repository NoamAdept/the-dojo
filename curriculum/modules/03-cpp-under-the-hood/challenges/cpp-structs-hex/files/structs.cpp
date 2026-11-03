#include <iomanip>
#include <iostream>
#include "structs.hpp"

void print_byte(uint8_t b)
{
    // TODO task 1
}

std::size_t sample_bytes(std::size_t count)
{
    // TODO task 2
    return 0;
}

reading make_reading(uint16_t channel, uint32_t freq_hz, uint8_t gain)
{
    reading r{};
    // TODO task 3
    return r;
}

void retune(reading* r, uint32_t freq_hz)
{
    // TODO task 4
}

uint8_t low_nibble(uint8_t b)
{
    // TODO task 5
    return 0;
}

uint8_t high_nibble(uint8_t b)
{
    return 0;
}

bool bit_is_set(uint8_t flags, unsigned bit)
{
    return false;
}

uint16_t read_be16(const uint8_t* p)
{
    // TODO task 6
    return 0;
}

uint32_t read_le32(const uint8_t* p)
{
    // TODO task 7
    return 0;
}
