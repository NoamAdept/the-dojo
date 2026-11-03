#include <iostream>

int main(int argc, char* argv[])
{
    if (argc < 2) {
        std::cout << "usage: ./greet NAME\n";
        return 1;
    }
    std::cout << "Hello, " << argv[1] << "!\n";
    return 0;
}
