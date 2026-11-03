# Parse Length-Prefixed Records: lesson

### Records

A very common binary format is **TLV** (type, length, value). The records sit one after another in one buffer (a block of bytes in memory). Each record looks like this:

```
byte 0   type      what kind of record this is
byte 1   length    how many payload bytes follow (0 to 255)
then     payload   exactly "length" bytes of data
```

Here is a buffer of 7 bytes that holds 2 records:

```
05 02 aa bb   07 01 cc
|  |  |___|   |  |  |
|  |  payload type 7, length 1, payload cc
|  length 2
type 5
```

A record with length 0 is fine. It is just its 2 header bytes.

The buffer may end in the middle of a header or a payload. Then the input is **truncated** (cut short). Your code must refuse it.

### Walk with an offset

Keep a `std::size_t offset`. It says where the next record starts.

- `data[offset]` is its type.
- `data[offset + 1]` is its length.
- `data + offset + 2` is a pointer to its payload.

The last one uses **pointer arithmetic**: when you add n to a pointer, it moves n items forward.

After each record, move the offset forward by `2 + length`.

### Never read outside the buffer

A length byte is a promise made by the input. It is not a guarantee. So check before every read:

- Before you read the 2 header bytes, make sure 2 bytes are left.
- Before you pass on the payload, make sure `length` bytes are left.

Write the check as `length <= size - offset` (when you already know `offset <= size`). Do not write `offset + length <= size`. With unsigned numbers, the subtraction form cannot wrap around.

### Calling the callback

A callback is a function that you get from other code, and that your code calls. `records.hpp` has:

```cpp
using record_visitor = void (*)(uint8_t type, const uint8_t* payload, std::size_t length, void* context);
```

Your parser gets a function like this as `visit`. It calls `visit` once for each complete record. It passes `context` along without changing it:

```cpp
visit(type, data + offset + 2, length, context);
```

### Writing your own callback

In task 3 you are on the other side. You write a visitor and give it to `parse_records`. Its parameters must match `record_visitor` exactly.

If you do not need a parameter, leave out its name. Then the compiler will not complain that it is unused:

```cpp
void count_one(uint8_t, const uint8_t*, std::size_t, void* context)
{
    int* n = static_cast<int*>(context);
    *n += 1;
}
...
int n = 0;
parse_records(data, size, count_one, &n);   // &n travels to count_one as context
```

### How this challenge works

Write your code in `records.cpp`. `records.hpp` is the header. It lists the functions so other files know they exist. Do not change it.

Each function has a `// TODO task N` comment. Delete the comment when you write the code. This tells `./check` that the task is started.

`./check` compiles your file together with a hidden test program. It uses `g++ -std=c++17 -Wall -Wextra -Werror` plus **sanitizers** (`-fsanitize=address,undefined`). Sanitizers are safety checks. They stop the program with a report at the moment it does one of these things:

- reads memory it should not
- follows a `nullptr`
- does arithmetic the C++ rules do not allow

Unused parameters are allowed here. So an unfinished task does not block the other tasks.

Do you want to try your functions yourself? Make a file `try.cpp` with `#include "records.hpp"` and a `main`. Then run `g++ -std=c++17 -Wall -Wextra try.cpp records.cpp -o try && ./try`.

### New words

- TLV: type, length, value. Records that say how long they are.
- record: one group of type, length and payload inside the buffer.
- payload: the data part of a record.
- truncated: cut short. The data ends too early.
- offset: how far into the buffer you are, in bytes.
- pointer arithmetic: `data + n` points n items further forward.
- callback: a function you give to other code, so that code can call it.
