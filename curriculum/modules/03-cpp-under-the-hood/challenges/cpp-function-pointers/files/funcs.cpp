#include "funcs.hpp"

int add(int a, int b)
{
    return a + b;
}

int mul(int a, int b)
{
    return a * b;
}

int apply(int_op op, int a, int b)
{
    // TODO task 2
    return 0;
}

int_op pick_op(char symbol)
{
    // TODO task 3
    return nullptr;
}

void visit_all(const int* values, std::size_t count, int_visitor visit, void* context)
{
    // TODO task 4
}

void update_stats(int value, void* context)
{
    // TODO task 5
}

std::size_t bytes_left(std::size_t size, std::size_t offset)
{
    // TODO task 6
    return 0;
}

bool read_be16_at(const uint8_t* buf, std::size_t size, std::size_t offset, uint16_t* out)
{
    // TODO task 7
    return false;
}
