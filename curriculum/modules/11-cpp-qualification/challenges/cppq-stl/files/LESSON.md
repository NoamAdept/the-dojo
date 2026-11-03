# STL Containers, Algorithms and Iterators: lesson

### 1. `std::vector`: The Dynamic Array

A C-array like `int a[10]` has a fixed size. A `std::vector` is different. It grows while the program runs (it is dynamic). Use it as your default container about 90% of the time.

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> numbers = {10, 20};
    
    // Add elements
    numbers.push_back(30);
    numbers.push_back(40);
    
    // Access
    std::cout << "Size: " << numbers.size() << std::endl;
    std::cout << "First: " << numbers[0] << std::endl;
    std::cout << "Last: " << numbers.back() << std::endl;
    
    return 0;
}
```

### 2. Vector Capacity vs Size

You must understand how a vector allocates (reserves) memory.
- **Size**: the number of elements it holds now.
- **Capacity**: the amount of memory it has reserved now.

Sometimes `size` grows past `capacity`. Then the vector reallocates. It moves everything to a bigger block of memory. This costs time. If you know the size before you start, call `reserve()`. This avoids the cost.

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v;
    v.reserve(100); // Allocate memory for 100 ints upfront
    
    std::cout << "Size: " << v.size() << ", Capacity: " << v.capacity() << std::endl;
    
    v.push_back(1);
    std::cout << "Size: " << v.size() << ", Capacity: " << v.capacity() << std::endl;
    
    return 0;
}
```

### 3. Iterators

An iterator is like a general pointer. With iterators, you can walk through *any* standard container in the same way.
- `begin()`: an iterator to the first element.
- `end()`: an iterator to the place *after the last* element (past-the-last).

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<std::string> fruits = {"Apple", "Banana", "Cherry"};
    
    std::vector<std::string>::iterator it;
    for (it = fruits.begin(); it != fruits.end(); ++it) {
        std::cout << *it << " "; // Dereference like a pointer
    }
    std::cout << std::endl;
    return 0;
}
```

### 4. Range-Based For Loop

This is modern C++ syntax for iterators. It is "syntax sugar": a shorter way to write the same thing. Use it for simple loops through a container.

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> nums = {1, 2, 3};
    
    for (int n : nums) {
        std::cout << n << " ";
    }
    return 0;
}
```

### 5. `std::map` (Ordered Dictionary)

A map stores Key-Value pairs. Each key is unique. The keys are kept **Sorted**. Inside, a map is a tree (usually a Red-Black Tree).
- Insert and find take O(log n) time. (Big-O notation: the time grows with log of n, the number of elements.)

```cpp
#include <iostream>
#include <map>
#include <string>

int main() {
    std::map<std::string, int> ages;
    ages["Alice"] = 25;
    ages["Bob"] = 30;
    
    // Keys are sorted alphabetically automatically
    for (const auto& pair : ages) {
        std::cout << pair.first << ": " << pair.second << std::endl;
    }
    return 0;
}
```

### 6. `std::unordered_map` (Hash Map)

It also stores Key-Value pairs. But the keys are **Unsorted**. Inside, it is a hash table.
- Insert and find take O(1) time on average. (The time does not grow with the number of elements.)
- Use it when you need speed and the order does not matter.

```cpp
#include <iostream>
#include <unordered_map>

int main() {
    std::unordered_map<std::string, int> stock;
    stock["Apple"] = 50;
    stock["Banana"] = 100;
    
    if (stock.find("Apple") != stock.end()) {
        std::cout << "Apple in stock!" << std::endl;
    }
    return 0;
}
```

### 7. `std::set`

A set stores only unique elements. It keeps them sorted. It is good for deduplication (removing copies).

```cpp
#include <iostream>
#include <set>

int main() {
    std::set<int> unique_nums;
    unique_nums.insert(10);
    unique_nums.insert(10); // Duplicate ignored
    unique_nums.insert(5);
    
    // Prints 5 10 (Sorted!)
    for (int n : unique_nums) std::cout << n << " ";
    return 0;
}
```

### 8. Algorithms: Sorting

The `<algorithm>` header has standard functions like `sort`, `reverse`, `min` and `max`.
- `std::sort` usually uses Introsort. Introsort mixes 3 methods: QuickSort, HeapSort and InsertionSort. It is very fast.

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {4, 2, 5, 1, 3};
    std::sort(v.begin(), v.end());
    
    for(int n : v) std::cout << n << " ";
    return 0;
}
```

### 9. Algorithms: Finding

`std::find` searches a range for a value.

```cpp
#include <iostream>
#include <algorithm>
#include <vector>

int main() {
    std::vector<int> v = {10, 20, 30};
    auto it = std::find(v.begin(), v.end(), 20);
    
    if (it != v.end()) {
        std::cout << "Found 20!" << std::endl;
    } else {
        std::cout << "Not found" << std::endl;
    }
    return 0;
}
```

### 10. `std::pair` and `std::tuple`

These are simple containers for heterogeneous data (values of mixed types). Maps use `pair` inside.

```cpp
#include <iostream>
#include <utility>

int main() {
    std::pair<std::string, int> student = {"John", 90};
    std::cout << student.first << ": " << student.second << std::endl;
    return 0;
}
```

---

## New words

- **STL**: the Standard Template Library. Ready-made containers and algorithms.
- **container**: an object that stores data.
- **algorithm**: a function that does work on data, like sorting.
- **iterator**: an object that points to an element in a container.
- **capacity**: how much memory a vector has reserved.
- **reallocate**: move the data to a new, bigger block of memory.
- **hash table**: a way to store data so you can find a key very fast.
- **deduplication**: removing copies, so each value appears once.
