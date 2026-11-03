# Read a Compiler Error

**What you will learn:** how to read the message g++ gives you when your source file has a mistake. And how to fix the mistake.

Is this new for you? Read **LESSON.md** first. Or press **Lesson** in the app.

## Your tasks

Each file has exactly 1 mistake. For each file, do these steps:

- Compile it.
- Read the first `error:` line.
- Open the file at that line and fix it.
- Compile again. Repeat until g++ prints nothing.
- Run the program.

1. **oops1.cpp** must print `Line one` and `Line two`. Compile: `g++ -std=c++17 -Wall -Wextra oops1.cpp -o oops1`
2. **oops2.cpp** must print `Spelling matters`. Compile: `g++ -std=c++17 -Wall -Wextra oops2.cpp -o oops2`
3. **oops3.cpp** must print `Braces come in pairs`. Compile: `g++ -std=c++17 -Wall -Wextra oops3.cpp -o oops3`
4. **oops4.cpp** must print `Almost done`. Compile: `g++ -std=c++17 -Wall -Wextra oops4.cpp -o oops4`

Do not change the text that the programs print. For each file that still fails, `./check` shows the first error line from g++. It also gives a hint in plain English.

## Check your work

You can run `./check` as many times as you want. It lists each task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
