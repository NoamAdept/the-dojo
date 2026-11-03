#include <iostream>
#include <vector>

static int largest(const std::vector<int> &values) {
    int best = values[0];
    for (std::size_t i = 1; i <= values.size(); ++i) {
        if (values[i] > best) best = values[i];
    }
    return best;
}

int main() {
    std::vector<int> values = {4, 12, 7, -1};
    std::cout << "largest=" << largest(values) << '\n';
    return 0;
}
