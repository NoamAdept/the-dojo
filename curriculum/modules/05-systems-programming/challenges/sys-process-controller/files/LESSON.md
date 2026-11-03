# Control a Child Process: lesson

## Lesson

Your shell runs every command you type in this way:

1. It forks a child (makes a copy of itself).
2. The child turns itself into the new program.
3. The shell waits for the child to end.

**fork** (from the pipes challenge) makes a copy of the current process.
`fork()` returns 0 in the child. In the parent, it returns the child's
process ID.

**exec.** The `exec` family of calls *replaces* the program in the
current process with another program from disk. It is the same process,
with the same ID, but with completely new code. `execl` takes these
arguments:

1. the path of the program,
2. then each argument as a separate string,
3. then a null pointer at the end.

```cpp
execl("/bin/ls", "ls", "-l", static_cast<char *>(nullptr));
```

- First `"/bin/ls"`: the file to run.
- Then `"ls"`: by tradition, argument 0 is the name of the program itself.
- Then the real arguments (`"-l"`).
- Then a null pointer to mark the end.

`execl` accepts any number of arguments. So it cannot know their type.
`static_cast<char *>(nullptr)` means "a text pointer that points
nowhere". This is exactly the end marker that `execl` looks for.

If `execl` works, it **never returns**. The old code is gone. So a line
after it only runs if `execl` fails. Put `std::perror("execl"); _exit(127);`
there.

**waitpid.** The parent waits for that one child. It also collects how
the child ended:

```cpp
int status;
if (waitpid(pid, &status, 0) == -1) { std::perror("waitpid"); return 1; }
if (WIFEXITED(status)) {
    std::cout << "it exited with code " << WEXITSTATUS(status) << '\n';
}
```

`&status` passes the address of `status` (as in C++ Under the Hood).
Then `waitpid` can fill it in. `status` holds several facts inside one
int. Do not print it directly. Use the macros from `<sys/wait.h>`:

- `WIFEXITED(status)` is true if the child ended normally.
- `WEXITSTATUS(status)` then gives its exit code. 0 means success.

**What the check looks for.** The output must contain 2 things:

1. the child's own `child_ok` line,
2. after it, a line from the parent in exactly this form. Use the exit
   code that you got from `WEXITSTATUS`:

```
child_status=0
```

Tip: `std::cout` text can wait in a buffer (memory where text waits
before it is written). If the parent prints something before `fork`,
use `std::endl` or `std::flush`. Then the text is not printed 2 times.

### New words

- **exec / execl**: replace the current program with another one.
- **argument 0 (`argv[0]`)**: by convention, the name of the program itself.
- **null pointer**: a pointer that points nowhere. It ends the argument list of `execl`.
- **waitpid**: wait for one specific child and collect its status.
- **exit status / exit code**: the number a program ends with. 0 means success.
- **macro**: a name like `WEXITSTATUS` that the compiler replaces with code.
- **buffer (std::cout)**: memory where text waits before it is written.

## Offline help

- `man 3 exec` (offline: `execl` and friends), `man 2 waitpid`, `man 2 fork`
