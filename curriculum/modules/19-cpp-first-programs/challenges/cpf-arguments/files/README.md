# Input from the Command Line

**What you will learn:** how your program can read the words that are typed after its name. For example, `ls -l` reads `-l`.

Is this new for you? Read **LESSON.md** first. Or press **Lesson** in the app.

## Your tasks

There are 2 small programs. Compile each one with its own name:

```
$ g++ -std=c++17 -Wall -Wextra greet.cpp -o greet
$ ./greet Ada
Hello, Ada!
$ g++ -std=c++17 -Wall -Wextra add.cpp -o add
$ ./add 3 4
7
```

1. **greet.cpp**: `./greet NAME` prints `Hello, NAME!` for any name. It exits with status 0.
2. **greet.cpp**: `./greet` with no name prints exactly `usage: ./greet NAME`. It exits with status 1. If there are more words after the name, the program does not use them.
3. **add.cpp**: `./add A B` prints the sum of the 2 whole numbers A and B. Examples: `./add 3 4` prints `7`. `./add -10 4` prints `-6`.
4. **add.cpp**: make it add **any** count of numbers. Use a loop over the words from argv[1] to argv[argc - 1]. `./add 1 2 3 4` prints `10`. `./add` with no numbers prints `0`.
5. **add.cpp**: if a word is not a number, print exactly `not a number: WORD` (with that word). Then exit with status 1. Example: `./add 3 abc` prints `not a number: abc`.

## Check your work

You can run `./check` as many times as you want. It lists each task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
