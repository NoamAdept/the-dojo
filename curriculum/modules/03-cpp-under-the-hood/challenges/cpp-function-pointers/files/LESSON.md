# Type Aliases, Function Pointers and Bounds Checks: lesson

### A new name for a type

`using NEW = OLD;` makes `NEW` another name for the type `OLD`. This is called a **type alias**. It does not create a new type. It is only a second name that makes code easier to read.

In system headers you will also see the older form `typedef OLD NEW;`. Both mean the same thing:

```cpp
using hertz = uint32_t;
typedef uint32_t hertz;       // same thing, older spelling
hertz centre = 433920000;     // exactly the same as uint32_t centre = ...
```

### Function pointers

A function is also stored in memory. So you can keep its address in a variable. This variable is a **function pointer**.

Its type looks like the function's first line, with `(*)` in place of the name. This is hard to read. So people almost always give the type a name. `funcs.hpp` has:

```cpp
using int_op = int (*)(int, int);   // int_op = "pointer to a function taking two ints, returning int"
int add(int a, int b);
```

A function's name on its own (without `()`) is its address. You call a function through the pointer in the same way as a normal function:

```cpp
int_op f = add;         // f now points at add
int x = f(2, 3);        // calls add(2, 3), x is 5
f = mul;
x = f(2, 3);            // now calls mul, x is 6
if (f == nullptr) ...   // a function pointer can be nullptr, meaning "no function"
```

Why is this useful? One piece of code can do different jobs. The job depends on which function you give it. You pass a function in, and other code calls it. This function is a **callback**.

Everyday C++ also has `std::function`. It can hold more kinds of things that you can call. But low-level libraries and system calls use plain function pointers. You will also see them in gdb.

### void*: a pointer to anything

`void*` is a pointer with no type. It can hold the address of any data. Any data pointer turns into a `void*` by itself.

Going back is not automatic. You must **cast** it with `static_cast`. The cast tells the compiler: "trust me, this really points at an int":

```cpp
int n = 0;
void* anything = &n;                          // forget the type for a while
int* back = static_cast<int*>(anything);      // back to its real type
*back += 1;                                   // n is now 1
```

Callbacks use this all the time. The code that calls your callback does not know what your data looks like. It does not need to know. It only passes a `void* context` along. Your callback casts it back:

```cpp
using int_visitor = void (*)(int value, void* context);

void count_big(int value, void* context)
{
    std::size_t* counter = static_cast<std::size_t*>(context);
    if (value > 100) *counter += 1;
}
```

You must cast back to the type that was really passed in. If you choose the wrong type, the compiler will not stop you. The program just does the wrong thing.

### Unsigned sizes and bounds checks

Sizes and positions in memory use `std::size_t`. This type is **unsigned**: it can never be negative. If a value goes below zero, it **wraps around** to a huge number:

```cpp
std::size_t size = 3, offset = 5;
std::size_t left = size - offset;    // NOT -2: it is 18446744073709551614 on a 64-bit Pi
```

So always compare first. Then subtract.

Say you want to read `need` bytes at `offset` from a buffer of `size` bytes. Before you read, this check is safe:

```cpp
if (offset > size || need > size - offset) {
    return false;               // not enough bytes: do not read
}
```

Why not write `offset + need > size`? Because `offset` may be huge, for example if it comes from a damaged file. Then `offset + need` wraps around to a small number. So the check passes when it should fail.

The form above never wraps. It only calculates `size - offset` when `offset <= size`.

`SIZE_MAX` (from `<cstdint>`) is the biggest possible `std::size_t`.

### How this challenge works

Write your code in `funcs.cpp`. `funcs.hpp` is the header. It lists the functions so other files know they exist. Change it only for task 1.

Each function has a `// TODO task N` comment. Delete the comment when you write the code. This tells `./check` that the task is started.

`./check` compiles your file together with a hidden test program. It uses `g++ -std=c++17 -Wall -Wextra -Werror` plus **sanitizers** (`-fsanitize=address,undefined`). Sanitizers are safety checks. They stop the program with a report at the moment it does one of these things:

- reads memory it should not
- follows a `nullptr`
- does arithmetic the C++ rules do not allow

Unused parameters are allowed here. So an unfinished task does not block the other tasks.

Do you want to try your functions yourself? Make a file `try.cpp` with `#include "funcs.hpp"` and a `main`. Then run `g++ -std=c++17 -Wall -Wextra try.cpp funcs.cpp -o try && ./try`.

### New words

- `using` / `typedef`: give an existing type a new name (a type alias).
- function pointer: a variable that holds the address of a function.
- callback: a function you give to other code, so that code can call it.
- `void*`: a pointer to data of any type.
- `static_cast<T*>(p)`: turns a `void*` back into a pointer of its real type.
- context: a `void*` that is passed to a callback, so the callback can keep its own data.
- wrap around: when an unsigned number goes below 0 (or above its maximum), it jumps to the other end.
- bounds check: a check that a position is inside a buffer, before you read it.
