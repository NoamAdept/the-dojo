#include <iostream>
#include <string>

int main(int argc, char* argv[])
{
    int total = 0;
    for (int i = 1; i < argc; i++) {
        try {
            total += std::stoi(argv[i]);
        } catch (...) {
            std::cout << "not a number: " << argv[i] << "\n";
            return 1;
        }
    }
    std::cout << total << "\n";
    return 0;
}
