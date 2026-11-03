// controller.cpp: start /bin/echo child_ok in a child process and report how it ended.
#include <sys/wait.h>  // waitpid, WIFEXITED, WEXITSTATUS
#include <unistd.h>    // fork, execl, _exit
#include <cstdio>      // std::perror
#include <iostream>

int main() {
    // TODO 1: pid_t pid = fork(); on -1: std::perror("fork"), return 1.
    // TODO 2: child (pid == 0):
    //           execl("/bin/echo", "echo", "child_ok", static_cast<char *>(nullptr));
    //         execl only comes back if it failed: std::perror("execl"); _exit(127);
    // TODO 3: parent: int status; waitpid(pid, &status, 0) (check for -1),
    //         then if WIFEXITED(status) print  child_status=<WEXITSTATUS(status)>
    //         and return 0.
    return 2;
}
