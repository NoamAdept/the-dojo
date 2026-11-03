# Structs That Do Things

**What you will learn:** how to make your own type with `struct`. You will also learn how to put functions inside it (member functions). Then the data and the code that uses the data are in one place.

Is this new to you? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

### How this challenge works

Write your code in `tasks.h`. Every function is already there. Each one has an empty body and a comment that says what it should do. Each file in `tests/` checks one task. `./check` compiles every test with `g++ -std=c++17` and runs it. Then it tells you in plain words what is still wrong.

The struct `Rectangle` with `width` and `height` is already in `tasks.h`. Fill in its methods.

1. **area**: return width times height.
2. **perimeter**: return the distance all the way around the rectangle: `2 * (width + height)`.
3. **scale**: multiply both width and height by `factor`. This one changes the rectangle.
4. **isSquare**: return `true` when width and height are equal.
5. **makeSquare**: this is a free function (a function outside the struct). It returns a Rectangle. The width and the height are both `side`.

## Check your work

Run `./check` as many times as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
