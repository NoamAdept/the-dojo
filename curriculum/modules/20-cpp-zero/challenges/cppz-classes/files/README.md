# Classes: Private Data and Constructors

**What you will learn:** how a `class` hides its data with `private:`. You will also learn how a class sets itself up with a constructor.

With the struct from the last challenge, anyone can write `r.width = -5;`. Nothing stops them. A **class** lets you hide fields. Then only the methods of the class itself can use them. So the methods can make sure that the data is always correct.

```cpp
class Counter {
public:                       // everyone may use what follows
    Counter(int start) {      // constructor: runs when a Counter is made
        count = start;
    }
    void increment() { count = count + 1; }
    int value() { return count; }

private:                      // only Counter's own methods may use what follows
    int count;
};

Counter c(5);                 // runs the constructor with start = 5
c.increment();
std::cout << c.value() << std::endl;   // 6
// c.count = 99;              // compile error: count is private
```

- `public:` and `private:` are labels. Everything below a label has that access. This continues until the next label.
- A **constructor** is a special method. It has the same name as the class and no return type. It runs automatically when you make an object, like `Counter c(5);`. Its job is to give every field a good starting value.
- A method that only returns a private field, like `value()`, is often called a **getter**.

`struct` and `class` are almost the same thing in C++. There is only 1 difference:

- In a `struct`, everything is public unless you say something else.
- In a `class`, everything is private unless you say something else.

People use `struct` for simple groups of data. They use `class` when there are rules to protect.

Is this new to you? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

### How this challenge works

Write your code in `tasks.h`. Every function is already there. Each one has an empty body and a comment that says what it should do. Each file in `tests/` checks one task. `./check` compiles every test with `g++ -std=c++17` and runs it. Then it tells you in plain words what is still wrong.

1. **Counter constructor and value**: make the constructor store `start` in `count`. Make `value()` return `count`.
2. **increment**: add 1 to `count`.
3. **Make count private**: now `count` is under `public:`. Add a `private:` label above it. Then code outside the class cannot use it.
4. **Radio basics**: add a private `double` field to `Radio`. This field holds the frequency.
   - The constructor stores `startMhz` in it.
   - `frequency()` returns it.
   - `tune(newMhz)` changes it.
5. **Radio rules**: only 88.0 to 108.0 MHz is allowed (88.0 and 108.0 are both allowed). `tune` ignores any value outside that range. If `startMhz` is outside the range, the constructor uses 88.0.

## Check your work

Run `./check` as many times as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
