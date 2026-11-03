# Copy with File Descriptors: lesson

## Lesson

**System calls.** Your program cannot use the disk by itself. It asks
the operating system to do it. The core part of the operating system is
the *kernel*. Each request from a program to the kernel is a
*system call*. You used `std::cout` and `std::ifstream` in the earlier
C++ modules. They are helpers built on top of a few basic system calls.
In this module you write low-level C++ that talks to Linux directly.
You use those basic calls yourself.

These calls are called *POSIX* calls. POSIX is a standard. Linux, macOS
and other Unix-like systems all follow it. So the same code works on all
of them.

**File descriptors.** When you open a file, the kernel gives you back a
small whole number. This number is the *file descriptor* (fd). After
that, you say "read from fd 3". You do not use the file name again.
Every process starts with 3 file descriptors:

- 0 is standard input (the keyboard).
- 1 is standard output (the screen).
- 2 is standard error (where error messages go).

`std::cout` writes to fd 1. `std::cerr` writes to fd 2.

**Arguments to main.** The command `./copy input.txt output.txt` gives
your program 2 words. C++ gives them to you through the parameters of
`main`:

```cpp
int main(int argc, char *argv[])
// argc = 3, argv[0] = "./copy", argv[1] = "input.txt", argv[2] = "output.txt"
```

- `argc` is the number of words. The program name counts too.
- `argv` is the list of words. Each word is a plain low-level text
  string (`char *`).

You can pass these words straight to `open`. You can also turn one into
a `std::string` with `std::string name = argv[1];`. Check `argc` before
you use `argv[1]` and `argv[2]`.

**The four calls.** They come from `<fcntl.h>` and `<unistd.h>`:

```cpp
int fd = open("notes.txt", O_RDONLY);                          // open for reading
int out = open("new.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644); // write; create; empty it first
ssize_t got = read(fd, buf, sizeof buf);   // read UP TO sizeof buf bytes into buf
ssize_t put = write(out, buf, got);        // write got bytes from buf
close(fd);                                 // give the fd back
```

- The flags (options for `open`) are:
  - `O_RDONLY`: read only.
  - `O_WRONLY`: write only.
  - `O_CREAT`: create the file if it does not exist.
  - `O_TRUNC`: if the file exists, make it empty first.
  - `|` combines flags.
- `0644` (used with `O_CREAT`) sets the permissions of the new file. The
  owner can read and write. Everyone else can only read. The 0 at the
  start means it is an octal number (base 8).
- `buf` is a plain array of bytes, for example `char buf[4096];`.
  `sizeof buf` is its size in bytes (4096). These calls work with raw
  bytes. That is why they take an array and a count, not a
  `std::string`.
- `ssize_t` is a whole-number type. It can also be negative.

**Return values matter.**

- `open` returns -1 if it fails.
- `read` returns the number of bytes it really got. This can be fewer
  than you asked for. It returns **0 at the end of the file**. It
  returns -1 on error.

So copying is a loop:

1. Read a chunk.
2. Write exactly that many bytes.
3. Repeat until `read` returns 0.

When a call fails, use `std::perror("open")` (from `<cstdio>`). It
prints a clear reason to stderr, for example
`open: No such file or directory`.

Return 0 from `main` on success. Return another number (like 1) on
failure. `./run` stops if the exit code is not 0.

Try it. `./run` does these things:

1. It builds your program.
2. It creates `input.txt`.
3. It runs your copy.
4. It compares the 2 files with `cmp`. `cmp` prints nothing when the
   files are the same.

The checker also does 3 more tests:

- It copies a large binary file.
- It copies over an existing file that is longer.
- It tries a source file that does not exist.

### New words

- **kernel**: the core of the operating system. It controls the hardware and the files.
- **system call**: a request from a program to the kernel.
- **POSIX**: the shared standard for Unix-like systems. `open`, `read` and `write` are POSIX calls.
- **file descriptor (fd)**: a small number that stands for an open file.
- **stdin / stdout / stderr**: fds 0, 1 and 2.
- **argc / argv**: the count and the list of command-line words given to `main`.
- **flag (for open)**: an option like `O_CREAT`. You combine flags with `|`.
- **octal**: base 8. Permissions like `0644` are written in octal.
- **end of file (EOF)**: when `read` returns 0, there is nothing left to read.
- **exit code**: the number that `main` returns. 0 means success.
- **binary file**: a file of raw bytes, not text.

## Offline help

- `man 2 open`, `man 2 read`, `man 2 write`, `man 2 close` (offline; section 2 is system calls)
