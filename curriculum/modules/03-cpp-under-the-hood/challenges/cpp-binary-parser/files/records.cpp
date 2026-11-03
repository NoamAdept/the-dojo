#include "records.hpp"

bool parse_records(const uint8_t* data, std::size_t size, record_visitor visit, void* context)
{
    // TODO task 1: walk the records and call visit for each one
    // TODO task 2: return false (before reading) when the buffer ends too early
    return false;
}

int count_records(const uint8_t* data, std::size_t size)
{
    // TODO task 3
    return 0;
}
