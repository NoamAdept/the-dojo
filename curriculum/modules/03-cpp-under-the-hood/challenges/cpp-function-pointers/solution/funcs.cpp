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
    return op(a, b);
}

int_op pick_op(char symbol)
{
    if (symbol == '+') {
        return add;
    }
    if (symbol == '*') {
        return mul;
    }
    return nullptr;
}

void visit_all(const int* values, std::size_t count, int_visitor visit, void* context)
{
    for (std::size_t i = 0; i < count; i++) {
        visit(values[i], context);
    }
}

void update_stats(int value, void* context)
{
    stats* s = static_cast<stats*>(context);
    s->count += 1;
    s->sum += value;
}

std::size_t bytes_left(std::size_t size, std::size_t offset)
{
    if (offset >= size) {
        return 0;
    }
    return size - offset;
}

bool read_be16_at(const uint8_t* buf, std::size_t size, std::size_t offset, uint16_t* out)
{
    if (buf == nullptr || out == nullptr || bytes_left(size, offset) < 2) {
        return false;
    }
    *out = static_cast<uint16_t>((buf[offset] << 8) | buf[offset + 1]);
    return true;
}
