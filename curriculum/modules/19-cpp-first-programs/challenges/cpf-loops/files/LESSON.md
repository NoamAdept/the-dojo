# Repeating: while and for: lesson

### while: repeat while a condition is true

```cpp
int i = 1;
while (i <= 3) {
    std::cout << i << "\n";
    i = i + 1;
}
// prints 1, 2, 3 on separate lines
```

How it works:

1. C++ checks the condition.
2. If the condition is true, C++ runs the block. Then it goes back to step 1.
3. When the condition is false, C++ goes on to the code after the loop.

Each time C++ runs the block is called an **iteration**.

Sometimes the condition never becomes false. Then the loop never stops. This is an **infinite loop**. Press `Ctrl+C` to stop a program like this. `./check` stops it after 5 seconds.

### Shorter ways to write updates

| Short | Means |
|---|---|
| `i++` | `i = i + 1` |
| `i--` | `i = i - 1` |
| `total += x` | `total = total + x` |
| `n /= 10` | `n = n / 10` |
| `p *= 2` | `p = p * 2` |

### for: the counting loop

Programs often count from a start number to an end number. So C++ has a special loop for this:

```cpp
for (int i = 1; i <= 3; i++) {
    std::cout << i << "\n";
}
```

There are 3 parts between the parentheses. A `;` separates them:

1. `int i = 1`: C++ does this once, at the start.
2. `i <= 3`: the condition. C++ checks it before each iteration.
3. `i++`: C++ does this after each iteration.

This loop does exactly the same work as the while loop above.

### The accumulator pattern

Sometimes you want to add up many numbers. Keep a running total in a variable that starts at 0. This variable is called an **accumulator**:

```cpp
int total = 0;
for (int i = 1; i <= 4; i++) {
    total += i;
}
// total is now 1 + 2 + 3 + 4 = 10
```

To multiply many numbers, start the accumulator at 1, not 0. (Any number times 0 is 0.)

### Functions that return nothing: void

Some functions do a job (like printing) and have no result. Their return type is `void`. `void` means "nothing". These functions do not need a `return` line:

```cpp
void say_hi()
{
    std::cout << "hi\n";
}
```

To print a single character, send a char: `std::cout << '*';`.

### New words

- loop: code that repeats.
- while: repeats its block while its condition is true.
- for: a counting loop. It has the start, the condition and the update in one line.
- iteration: one time through the block of the loop.
- infinite loop: a loop whose condition never becomes false. It never stops.
- accumulator: a variable that keeps a running total.
- `++`, `+=`: short ways to write "add 1" and "add this".
- void: "nothing". A void function returns no value.
