#pragma once
#include <cstddef>
#include <cstdint>

// A visitor gets: the record's type byte, a pointer to its payload, the payload length, and the caller's context.
using record_visitor = void (*)(uint8_t type, const uint8_t* payload, std::size_t length, void* context);

// Calls visit once per complete record, in order.
// Returns true when every byte belongs to a complete record, false when the input is cut short.
bool parse_records(const uint8_t* data, std::size_t size, record_visitor visit, void* context);  // tasks 1 and 2

// Number of complete records, or -1 when the input is cut short. Uses parse_records.
int count_records(const uint8_t* data, std::size_t size);  // task 3
