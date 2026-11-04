# Parent, Child, Pipe

`sys-pipes` · Orange Belt

**Goal:** Finish `pipe_demo.cpp` so a child process writes `samples=64` into a pipe, and the parent reads it, prints it once, and waits for the child.

**File `pipe_demo.cpp`**

```cpp
#include <sys/wait.h>  // wait
#include <unistd.h>    // pipe, fork, read, write, close, _exit
#include <cstdio>      // std::perror
#include <iostream>
#include <string>

int main() {
    int fds[2];
    if (pipe(fds) == -1) {
        std::perror("pipe");
        return 1;
    }
    pid_t pid = fork();
    if (pid == -1) {
        std::perror("fork");
        return 1;
    }
    if (pid == 0) {  // child: the writer
        close(fds[0]);
        const std::string msg = "samples=64";
        if (write(fds[1], msg.data(), msg.size()) == -1) std::perror("write");
        close(fds[1]);
        _exit(0);
    }
    close(fds[1]);
    std::string text;
    char buf[64];
    ssize_t got;
    while ((got = read(fds[0], buf, sizeof buf)) > 0) {
        text.append(buf, got);
    }
    if (got == -1) std::perror("read");
    close(fds[0]);
    wait(nullptr);
    std::cout << text << '\n';
    return 0;
}
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
