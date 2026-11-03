#include <iostream>
#include <iomanip>

int main()
{
    double price = 2.5;
    int count = 4;
    int sum = 7;
    int parts = 3;
    char grade = 'B';

    std::cout << "given: " << price << " " << count << " " << sum << " " << parts << " " << grade << "\n";

    // Task 1: print total=10.00 (price * count, two decimals)
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "total=" << price * count << "\n";

    // Task 2: print grade=B
    std::cout << "grade=" << grade << "\n";

    // Task 3: print next=C (the letter after grade)
    char next = grade + 1;
    std::cout << "next=" << next << "\n";

    // Task 4: print many=1 (a bool: is count greater than 3?)
    bool many = count > 3;
    std::cout << "many=" << many << "\n";

    // Task 5: print average=2.33 (sum / parts, two decimals)
    std::cout << "average=" << static_cast<double>(sum) / parts << "\n";

    return 0;
}
