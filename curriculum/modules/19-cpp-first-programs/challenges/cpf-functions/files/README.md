# Functions: Inputs and Outputs

**What you will learn:** how to make your own functions. Then you can give a calculation a name once and use it many times.

Is this new for you? Read **LESSON.md** first. Or press **Lesson** in the app.

## Your tasks

Open `tasks.cpp` and finish the functions:

1. `add(a, b)` returns a plus b. Example: `add(2, 3)` is 5.
2. `square(x)` returns x times x. Example: `square(4)` is 16.
3. `to_fahrenheit(celsius)` takes a double. It returns the temperature in Fahrenheit. The formula is: celsius times 9, divided by 5, plus 32. Example: `to_fahrenheit(100.0)` is 212.0.
4. **Write a full function yourself.** There is no stub for this one. Write `int perimeter(int width, int height)`. It returns the distance around a rectangle: 2 times width plus 2 times height. Put it above `main`. Example: `perimeter(3, 4)` is 14. Then add a line to `main` that prints `perimeter(3, 4) = 14`. Use your function to do this.
5. `sum_of_squares(a, b)` returns a squared plus b squared. **Call your `square` function** to do this. Example: `sum_of_squares(3, 4)` is 25.

## Check your work

You can run `./check` as many times as you want. It lists each task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
