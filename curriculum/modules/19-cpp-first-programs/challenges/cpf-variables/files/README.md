# Variables and Whole Numbers

**What you will learn:** how to store a number in a box with a name (a variable), how to calculate with it, and how to print it.

Is this new for you? Read **LESSON.md** first. Or press **Lesson** in the app.

## Your tasks

Open `numbers.cpp`. It already has the lines `int apples = 7;` and `int friends = 3;`. **Do not change these 2 lines.** `./check` puts other numbers into them. This way it can test that you use the variables, and not numbers that you typed.

For each task, add 1 `std::cout` line below the comment for that task. After each task, build again and run:

```
$ g++ -std=c++17 -Wall -Wextra numbers.cpp -o numbers
$ ./numbers
```

1. Print `apples=7`. Use the variable `apples`.
2. Print `total=10`. This is apples plus friends.
3. Print `each=2`. This is how many whole apples each friend gets (apples divided by friends).
4. Print `left=1`. This is how many apples are left over (the remainder).

When it works, `./numbers` prints the line that was already there. Then it prints your 4 lines.

## Check your work

You can run `./check` as many times as you want. It lists each task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
