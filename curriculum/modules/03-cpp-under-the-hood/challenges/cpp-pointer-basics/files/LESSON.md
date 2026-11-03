# Pointers: Addresses You Can Follow: lesson

### Addresses

Memory is one long row of bytes. Every byte has a number. This number is its **address**.

Every variable lives somewhere in that row. `&score` ("address of score") tells you where:

```cpp
int score = 5;
std::cout << &score << "\n";    // something like 0x7ffd5c2a1b3c (hex, different every run)
```

### Pointers

A **pointer** is a variable that holds an address:

```cpp
int score = 5;
int* p = &score;              // p is a "pointer to int"; it holds the address of score
std::cout << *p << "\n";      // *p follows the pointer: prints 5
*p = 9;                       // writes 9 into score through the pointer
std::cout << score << "\n";   // prints 9
```

- `&` goes from a variable to its address.
- `*` goes from an address back to the value at that address.

Following a pointer like this is called **dereferencing**. The `*` in `int* p` is just part of the type name. It means "pointer to int".

### Pointers and references

You already know references. `int& r = score;` is another name for `score`.

A pointer is similar, but it is a separate variable that holds an address. It is different in 3 ways:

- You write `*` to reach the value.
- You can make it point somewhere else later.
- It can point at nothing.

Low-level code is full of pointers. This includes byte buffers (blocks of memory that hold data), hardware, system calls, and what you will see in gdb. That is why this module uses pointers.

### Changing the caller's variable

A normal parameter is a copy. So this function changes nothing for the caller:

```cpp
void add_ten(int x) { x = x + 10; }       // changes only its own copy
```

Give the function the address instead. Then it can reach the caller's variable:

```cpp
void add_ten(int* x) { *x = *x + 10; }
int n = 4;
add_ten(&n);          // pass the address of n; now n is 14
```

To swap 2 values, you need a place to keep one of them for a moment. Think of 2 cups of juice. To swap the juice, you need a third cup. In code: `int temp = first; first = second; second = temp;`

### A pointer to a row of values

A `std::vector<int>` keeps its items next to each other in one block of memory. Many functions only get 2 things: a pointer to the first item, and a count. `.data()` gives you that pointer.

A **raw array** like `int v[3] = {2, -1, 7};` is the simple version of the same idea. It is a fixed number of items next to each other, with no `.size()`. When you pass it to a function, it becomes a pointer to its first item.

On a pointer, `values[i]` still means "item number i, counting from 0":

```cpp
int total_of_two(const int* values) { return values[0] + values[1]; }

int v[3] = {2, -1, 7};
std::vector<int> w = {4, 5};
total_of_two(v);           // 1
total_of_two(w.data());    // 9
```

`const int*` means "this function promises not to change the items".

A pointer does not know how many items follow it. So you always pass the count too. You must never read `values[count]` or anything after it. Nothing stops you from doing this. The program just reads whatever memory is there. The checker's sanitizer stops the test if you do it.

`&values[i]` is the address of item `i`. You can also write it as `values + i`. When you add a number to a pointer, it moves forward by that many items.

### nullptr

`nullptr` is a pointer that points at nothing. If you follow it (`*p`), the program crashes. So when a pointer might be empty, check `if (p == nullptr)` first. A function that returns a pointer can return `nullptr` to say "not found".

### Header and source

`pointers.hpp` holds the **declarations**. A declaration is a function's return type, name and parameters, ending in `;`.

`pointers.cpp` holds the **definitions**. A definition is the same line with a body in `{ }`.

The `.cpp` file starts with `#include "pointers.hpp"`. The hidden test program does this too. So both agree on what the functions look like.

### How this challenge works

Write your code in `pointers.cpp`. `pointers.hpp` is the header. It lists the functions so other files know they exist. Do not change it.

Each function has a `// TODO task N` comment. Delete the comment when you write the code. This tells `./check` that the task is started.

`./check` compiles your file together with a hidden test program. It uses `g++ -std=c++17 -Wall -Wextra -Werror` plus **sanitizers** (`-fsanitize=address,undefined`). Sanitizers are safety checks. They stop the program with a report at the moment it does one of these things:

- reads memory it should not
- follows a `nullptr`
- does arithmetic the C++ rules do not allow

Unused parameters are allowed here. So an unfinished task does not block the other tasks.

Do you want to try your functions yourself? Make a file `try.cpp` with `#include "pointers.hpp"` and a `main`. Then run `g++ -std=c++17 -Wall -Wextra try.cpp pointers.cpp -o try && ./try`.

### New words

- address: the number of a place in memory.
- pointer: a variable that holds an address. `int*` is "pointer to int".
- `&` (address-of): gives the address of a variable.
- `*` (dereference): follows a pointer to the value it points at.
- raw array: a fixed number of values next to each other, like `int v[3]`.
- `.data()`: gives a pointer to the first item of a `std::vector`.
- `nullptr`: a pointer that points at nothing.
- declaration / definition: a function's first line ending in `;` / the same line with its body.
- sanitizer: a compiler option that catches memory mistakes while the program runs.
- buffer: a block of memory that holds data.
