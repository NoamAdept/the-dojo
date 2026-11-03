#pragma once
#include <cstddef>
#include <cstdint>

// TODO task 1: make `byte` another name for uint8_t here.

using int_op = int (*)(int, int);
int add(int a, int b);                       // already written
int mul(int a, int b);                       // already written
int apply(int_op op, int a, int b);          // task 2
int_op pick_op(char symbol);                 // task 3

using int_visitor = void (*)(int value, void* context);
void visit_all(const int* values, std::size_t count, int_visitor visit, void* context);  // task 4

struct stats {
    std::size_t count;
    long sum;
};
void update_stats(int value, void* context);  // task 5

std::size_t bytes_left(std::size_t size, std::size_t offset);                                // task 6
bool read_be16_at(const uint8_t* buf, std::size_t size, std::size_t offset, uint16_t* out);  // task 7
