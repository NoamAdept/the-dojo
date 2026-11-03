# Lists with std::vector

**What you will learn:** how to keep a list of values in a `std::vector`. You will also learn to loop over it with a range-based `for`.

One variable holds one value. But what if you have 100 signal readings, or a list of words? You do not want to make 100 variables. A `std::vector` (from `#include <vector>`) is one variable that holds a whole **list** of values. All the values have the same type. The vector grows when you add to it.

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v = {3, 1, 4};   // a list of ints, starting with 3 values
    v.push_back(1);                   // add 1 at the end: {3, 1, 4, 1}
    std::cout << v.size() << std::endl;   // 4
    std::cout << v[0] << std::endl;       // 3: the item at index 0, same [ ] as on a string
    return 0;
}
```

The `<int>` in angle brackets tells what the vector holds. `std::vector<double>` holds doubles. `std::vector<std::string>` holds strings. `push_back` and `size` are member functions, like `size()` on a string. `v.empty()` is `true` when the vector has no items.

Is this new to you? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

### How this challenge works

Write your code in `tasks.h`. Every function is already there. Each one has an empty body and a comment that says what it should do. Each file in `tests/` checks one task. `./check` compiles every test with `g++ -std=c++17` and runs it. Then it tells you in plain words what is still wrong.

1. **sumAll**: return the sum of all numbers in the vector. For an empty vector, return 0. Use a range-based `for`.
2. **countAbove**: return the count of numbers that are bigger than `limit`.
3. **makeRange**: return the vector `{1, 2, ..., n}`. For `n` of 0 or less, return an empty vector. Use `push_back`.
4. **largest**: return the biggest number in the vector. The vector always has at least one number. Hint: start with `v[0]`.
5. **longWords**: return a new vector. It has only the words with a length of at least `minLen`. Keep them in the same order.

## Check your work

Run `./check` as many times as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
