# Copy Through the FD

`sys-file-descriptors` · Orange Belt

**Goal:** Finish `copy.cpp` so `./copy SOURCE DEST` copies any file byte for byte using the POSIX calls `open`, `read`, `write` and `close`, and returns 1 with a message on any error.

**File `copy.cpp`**

```cpp
#include <fcntl.h>   // open and the O_... flags
#include <unistd.h>  // read, write, close
#include <cstdio>    // std::perror
#include <iostream>

int main(int argc, char *argv[]) {
    if (argc != 3) {
        std::cerr << "usage: ./copy SOURCE DEST\n";
        return 1;
    }
    int in = open(argv[1], O_RDONLY);
    if (in == -1) {
        std::perror("open");
        return 1;
    }
    int out = open(argv[2], O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (out == -1) {
        std::perror("open");
        close(in);
        return 1;
    }
    char buf[4096];
    int result = 0;
    while (true) {
        ssize_t got = read(in, buf, sizeof buf);
        if (got == 0) break;
        if (got == -1) { std::perror("read"); result = 1; break; }
        if (write(out, buf, got) != got) { std::perror("write"); result = 1; break; }
    }
    close(in);
    if (close(out) == -1) { std::perror("close"); result = 1; }
    return result;
}
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
