# Making Decisions: if and else: lesson

### Comparisons

A **comparison** asks a yes/no question about 2 values. The answer is a `bool`: `true` or `false`.

| Write | Means |
|---|---|
| `a == b` | a is equal to b (two `=` signs!) |
| `a != b` | a is not equal to b |
| `a < b`, `a > b` | less than, greater than |
| `a <= b`, `a >= b` | less or equal, greater or equal |

Be careful: one `=` means "store". Two `==` mean "compare". Many people write `if (x = 5)` by mistake. This is a very common bug. g++ warns you about it.

### if and else

```cpp
if (temperature > 30) {
    std::cout << "hot\n";
} else {
    std::cout << "not hot\n";
}
```

The **condition** goes in parentheses. If the condition is true, the first block runs. A block is the lines between braces. If the condition is false, the `else` block runs. You do not have to write the `else` part.

Sometimes you have more than 2 choices. Then add more choices with `else if`. C++ checks them from the top to the bottom. It runs only the first one that is true:

```cpp
if (n > 0) {
    return 1;
} else if (n < 0) {
    return -1;
} else {
    return 0;
}
```

### Combining conditions

- `&&` means AND: both must be true. `age >= 13 && age <= 19` is true for teenagers.
- `||` means OR: at least one must be true. `day == 6 || day == 7` is true at the weekend.
- `!` means NOT: `!(x > 5)` is true when x is not greater than 5.

### Functions that answer yes or no

A function can return a `bool`. You can return a comparison directly:

```cpp
bool is_teen(int age)
{
    return age >= 13 && age <= 19;
}
```

### Using the remainder

A number is even when you divide it by 2 and nothing is left over: `n % 2 == 0`.

### New words

- comparison: a yes/no question like `a < b`. The answer is true or false.
- condition: the comparison inside `if ( )`.
- if / else: run one block when the condition is true. Run another block when it is false.
- else if: an extra choice. C++ checks it only when all the choices above it were false.
- block: lines that are grouped inside `{` and `}`.
- `&&`, `||`, `!`: and, or, not.
