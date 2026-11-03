// C++ Qualification 05: pointers and references.
#pragma once
#include <string>

inline int* addressOf(int& v) { return &v; }

inline void doubleViaPointer(int* p) { *p *= 2; }

inline std::string walkCString(const char* s) {
    std::string out;
    for (const char* p = s; *p != '\0'; ++p) out += *p;
    return out;
}

inline std::string describe(const int* p) {
    if (p == nullptr) return "Null Pointer";
    return "Value is: " + std::to_string(*p);
}

inline void swap(int* a, int* b) {
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

inline void reverseArray(int* arr, int size) {
    for (int *start = arr, *end = arr + size - 1; start < end; ++start, --end) swap(start, end);
}

inline void findMinMax(const int* arr, int size, int* minOut, int* maxOut) {
    *minOut = *maxOut = arr[0];
    for (const int* p = arr + 1; p < arr + size; ++p) {
        if (*p < *minOut) *minOut = *p;
        if (*p > *maxOut) *maxOut = *p;
    }
}
