#pragma once
#include <cstddef>
#include <cstdint>

struct reading {
    uint16_t channel;
    uint32_t freq_hz;
    uint8_t gain;
};

void print_byte(uint8_t b);                                              // task 1
std::size_t sample_bytes(std::size_t count);                             // task 2
reading make_reading(uint16_t channel, uint32_t freq_hz, uint8_t gain);  // task 3
void retune(reading* r, uint32_t freq_hz);                               // task 4
uint8_t low_nibble(uint8_t b);                                           // task 5
uint8_t high_nibble(uint8_t b);                                          // task 5
bool bit_is_set(uint8_t flags, unsigned bit);                            // task 5
uint16_t read_be16(const uint8_t* p);                                    // task 6
uint32_t read_le32(const uint8_t* p);                                    // task 7
