// pipe_demo.cpp: a child process sends "samples=64" to its parent through a pipe.
#include <sys/wait.h>  // wait
#include <unistd.h>    // pipe, fork, read, write, close, _exit
#include <cstdio>      // std::perror
#include <iostream>
#include <string>

int main() {
    // TODO 1: int fds[2]; call pipe(fds). On -1: std::perror("pipe"), return 1.
    // TODO 2: pid_t pid = fork(); on -1: std::perror("fork"), return 1.
    // TODO 3: child (pid == 0): close the read end fds[0],
    //         write the text samples=64 into fds[1], close it, then _exit(0).
    // TODO 4: parent: close the write end fds[1], read into a char buffer,
    //         turn the bytes into a std::string, print it with std::cout and '\n',
    //         close fds[0] and wait(nullptr) for the child.
    return 2;
}
