# Variables and Whole Numbers: lesson

### Variables

A **variable** is a box in the computer's memory. The box has a name, and it holds a value. In C++, you must say the **type** of the value when you create the box. The type tells what kind of value the box holds. The type for whole numbers is `int`. Whole numbers have no decimal point. `int` is short for "integer".

```cpp
int apples = 7;
```

This line creates a box with the name `apples`. The box holds whole numbers. The line puts 7 in the box. When you create a variable, we say that you **declare** it. Later, you can put a new value in the box. Do not write `int` again:

```cpp
apples = 9;
```

Rules for names:

- A name can use letters, digits and `_`.
- A name cannot start with a digit.
- `apples`, `total_count` and `x2` are good names.
- Capital letters and small letters are different. `Apples` is a different name.

### Arithmetic

| Write | Means | Example (apples = 7) |
|---|---|---|
| `a + b` | add | `apples + 3` is 10 |
| `a - b` | subtract | `apples - 3` is 4 |
| `a * b` | multiply | `apples * 3` is 21 |
| `a / b` | divide | `apples / 3` is **2** |
| `a % b` | remainder | `apples % 3` is 1 |

Be careful! When you divide two `int`s, C++ removes the part after the decimal point. 7 / 3 is 2. It is not 2.33. This is called **integer division**.

The `%` operator gives you the part that is left over. This is the **remainder**: 7 = 3 * 2 + **1**.

You can store a result in a new variable:

```cpp
int doubled = apples * 2;
```

### Printing numbers

`std::cout` can also print numbers. You can send several things in one line. Repeat `<<` before each thing. They are printed one after the other, with no space between them:

```cpp
std::cout << "apples=" << apples << "\n";          // prints apples=7
std::cout << apples << " plus " << 3 << "\n";      // prints 7 plus 3
std::cout << "doubled=" << apples * 2 << "\n";     // prints doubled=14
```

Text in quote marks is printed exactly as you wrote it. A name without quote marks (like `apples`) prints the value that is inside that box.

On a line, everything after `//` is a **comment**. A comment is a note for people. The compiler does not read it.

### New words

- variable: a box with a name that holds a value, like `apples`.
- type: the kind of value that a variable holds. `int` means whole numbers.
- declare: create a variable, for example `int apples = 7;`.
- integer division: `/` between two ints. It removes the decimals (7 / 3 is 2).
- remainder: what `%` gives. It is the part that is left over after you divide (7 % 3 is 1).
- `<<` chain: `std::cout << a << b;` prints a, then b.
- comment: a note after `//`. g++ does not read it.
