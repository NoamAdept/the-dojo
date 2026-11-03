# Connect Parent and Child with a Pipe: lesson

## Lesson

**fork.** `fork()` makes an almost exact copy of the running process.
After the call, there are 2 processes. Both run the same code, from the
same place. The original process is the *parent*. The copy is the
*child*. The only difference is the value that `fork` returned:

```cpp
pid_t pid = fork();
if (pid == -1)      { std::perror("fork"); return 1; }  // failed, no child
else if (pid == 0)  { /* this is the CHILD */ }
else                { /* this is the PARENT; pid is the child's process ID */ }
```

- -1 means `fork` failed. There is no child.
- 0 means "you are the child".
- Any other number means "you are the parent". The number is the
  child's process ID.

Each process has its own copy of every variable. If the child changes a
variable, the parent's copy does not change. So the 2 processes need a
way to talk.

**pipe.** A pipe is a one-way tube for bytes. The kernel (the core of
the operating system) makes it. You give `pipe` an array of 2 ints. It
fills in 2 file descriptors (small numbers that stand for open files;
see the previous challenge):

```cpp
int fds[2];
if (pipe(fds) == -1) { std::perror("pipe"); return 1; }
// fds[0] is the READ end, fds[1] is the WRITE end
```

Bytes that you write into `fds[1]` come out of `fds[0]`, in the same
order. It is the same idea as `|` in the shell. Make the pipe
**before** `fork`. Then both processes get copies of both ends.

**Who closes what.** Each process closes the end that it does not use:

- The writer closes the read end.
- The reader closes the write end.

When every write end is closed, the reader's `read` returns 0 (end of
data). If a write end is still open, `read` waits forever.

**Sending and receiving text.** `write` needs raw bytes and a count. A
`std::string` gives you both:

- `.data()` is where its bytes start.
- `.size()` is how many bytes there are.

```cpp
const std::string msg = "hello";
write(fds[1], msg.data(), msg.size());
```

The reader gets bytes with `read`. `read` returns how many bytes
arrived. It returns 0 at the end and -1 on error. Collect the bytes in
a `std::string`. `text.append(buf, got)` adds exactly `got` bytes from
`buf`:

```cpp
std::string text;
char buf[64];
ssize_t got;
while ((got = read(fds[0], buf, sizeof buf)) > 0) {
    text.append(buf, got);
}
std::cout << text << '\n';
```

**Waiting.** The parent should call `wait(nullptr)` (from
`<sys/wait.h>`). This lets the child finish, and then the system cleans
it up. The child should end with `_exit(0)`. Then it stops at that
point and never runs the parent's code.

Tip: `std::cout` keeps text in a buffer (memory where text waits) before
it really writes it. Maybe you print something before `fork` without
`std::endl` or `std::flush`. Then the text that is not yet written is
copied into both processes. It may appear 2 times.

### New words

- **fork**: a system call that creates a copy of the current process.
- **parent / child**: the original process and the new copy.
- **pid_t**: the type that holds a process ID.
- **process ID**: the number that names a running process.
- **pipe**: a one-way channel for bytes, made by the kernel. It has a read end and a write end.
- **read end / write end**: `fds[0]` / `fds[1]` from `pipe`.
- **wait**: makes the parent pause until a child ends.
- **_exit**: ends this process at once, with an exit code.
- **buffer**: memory where data waits before it is used or written.

## Offline help

- `man 2 pipe` (offline; its EXAMPLES section shows a parent and child), `man 2 fork`, `man 2 wait`
- `man 7 pipe` (offline: how pipes behave)
