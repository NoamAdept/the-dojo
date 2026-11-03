#include <iostream>
#include <iomanip>
#include <string>

// Example: the larger of a and b
int larger(int a, int b)
{
    if (a > b) {
        return a;
    }
    return b;
}

// Task 1: the smaller of a and b
int smaller(int a, int b)
{
    if (a < b) {
        return a;
    }
    return b;
}

// Task 2: true when level is -60 or higher
bool is_strong(int level)
{
    return level >= -60;
}

// Task 3: total / count as a double
double average(int total, int count)
{
    return static_cast<double>(total) / count;
}

int main(int argc, char* argv[])
{
    int count = argc - 1;
    if (count < 1) {
        std::cout << "usage: ./report LEVEL...\n";
        return 1;
    }

    int total = 0;
    int low = 0;
    int high = 0;
    int strong = 0;
    for (int i = 1; i < argc; i++) {
        int level = 0;
        try {
            level = std::stoi(argv[i]);
        } catch (...) {
            std::cout << "not a number: " << argv[i] << "\n";
            return 1;
        }
        if (i == 1) {
            low = level;
            high = level;
        }
        low = smaller(low, level);
        high = larger(high, level);
        total += level;
        if (is_strong(level)) {
            strong++;
        }
    }

    std::cout << "readings: " << count << "\n";
    std::cout << "smallest: " << low << "\n";
    std::cout << "largest: " << high << "\n";
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "average: " << average(total, count) << "\n";
    std::cout << "strong: " << strong << "\n";
    return 0;
}
