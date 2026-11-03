# Functions: Inputs and Outputs: lesson

### What a function is

You already know one function: `main`. Your program starts there. A **function** is a piece of code with a name. It takes some inputs and does some work. It can give back one result. Think of a coffee machine: you put water and coffee in, and a cup of coffee comes out.

```cpp
int add(int a, int b)
{
    return a + b;
}
```

Read it from left to right:

- The first `int` is the **return type**. It is the type of the result that this function gives back.
- `add` is the name of the function.
- `(int a, int b)` are the **parameters**. These are the inputs. Each one has a type and a name. Inside the function, you use `a` and `b` like variables. (`main()` has empty parentheses because it needs no inputs.)
- `return a + b;` calculates the result. It gives the result back. Then it leaves the function at once.

### Calling a function

When you use a function, we say that you **call** it. Write its name. Then put the values in parentheses. These values are called **arguments**:

```cpp
int total = add(2, 3);                  // a is 2, b is 3, total becomes 5
std::cout << add(10, -4) << "\n";       // prints 6
```

A function can call another function:

```cpp
int add_three(int a, int b, int c)
{
    return add(add(a, b), c);
}
```

### Order is important

g++ reads your file from the top to the bottom. You must write a function **above** the place where you call it. If you do not, g++ says that the name "was not declared in this scope".

### How this file is organized

From now on, each challenge gives you a file `tasks.cpp`. It has **stub** functions. A stub is a function that is not finished. Its first line is already written, but its body only says `return 0;`. Your job is to change this into the real calculation.

`./check` calls your functions with many different inputs. Then it compares the results.

The `main` at the bottom is for you. It prints some examples, so you can test your work. Build it and run it like before:

```
$ g++ -std=c++17 -Wall -Wextra tasks.cpp -o tasks
$ ./tasks
```

g++ may warn "unused parameter" for stubs that you did not finish yet. The warning goes away when you use the parameter.

### New words

- function: a piece of code with a name, inputs and one result.
- parameter: an input of a function. It has a type and a name, like `int a`.
- argument: the real value that you give when you call a function, like the 2 in `add(2, 3)`.
- return type: the type of the result. You write it before the name of the function.
- return: gives back the result and leaves the function.
- call: use a function, for example `add(2, 3)`.
- stub: a function with a temporary body. You must finish it.
