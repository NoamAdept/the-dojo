# Decimals, Letters and Yes/No

**What you will learn:** how to store decimal numbers, single letters and yes/no answers. And how to print them in a clear way.

Is this new for you? Read **LESSON.md** first. Or press **Lesson** in the app.

## Your tasks

Open `types.cpp`. There are 5 lines that create `price`, `count`, `sum`, `parts` and `grade`. **Do not change these 5 lines.** `./check` puts other values into them.

For each task, add 1 line below its comment. After each task, build again and run:

```
$ g++ -std=c++17 -Wall -Wextra types.cpp -o types
$ ./types
```

1. Print `total=10.00`. This is price times count, with exactly 2 decimals.
2. Print `grade=B`.
3. Print `next=C`. This is the letter after `grade`. Do you see `next=67`? Then store the value in a `char` first.
4. Print `many=1`. Use a bool that is true when count is greater than 3. When count is not greater than 3, it prints `many=0`.
5. Print `average=2.33`. This is sum divided by parts, with 2 decimals. Do you see `average=2.00`? Then you have the integer-division problem from the lesson.

## Check your work

You can run `./check` as many times as you want. It lists each task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
