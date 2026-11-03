// copy.cpp: copy one file to another using the low-level POSIX calls
// that talk straight to Linux: open, read, write, close.
#include <fcntl.h>   // open and the O_... flags
#include <unistd.h>  // read, write, close
#include <cstdio>    // std::perror
#include <iostream>

int main(int argc, char *argv[]) {
    // TODO 1: if argc is not 3, print "usage: ./copy SOURCE DEST" to std::cerr
    //         and return 1.
    // TODO 2: open argv[1] read-only. If open returns -1: std::perror("open"), return 1.
    // TODO 3: open argv[2] with O_WRONLY | O_CREAT | O_TRUNC and permissions 0644.
    //         On -1: std::perror, close the first fd, return 1.
    // TODO 4: make a buffer (char buf[4096];) and loop:
    //           read up to sizeof buf bytes; 0 means the end, -1 means an error;
    //           write exactly the number of bytes read (check it for -1 too).
    // TODO 5: close both fds and return 0.
    (void)argc;  // these two lines only silence "unused" warnings; delete them
    (void)argv;
    return 2;
}
