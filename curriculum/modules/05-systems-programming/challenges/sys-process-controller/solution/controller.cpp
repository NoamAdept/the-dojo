// controller.cpp: start /bin/echo child_ok in a child process and report how it ended.
#include <sys/wait.h>  // waitpid, WIFEXITED, WEXITSTATUS
#include <unistd.h>    // fork, execl, _exit
#include <cstdio>      // std::perror
#include <iostream>

int main() {
    pid_t pid = fork();
    if (pid == -1) {
        std::perror("fork");
        return 1;
    }
    if (pid == 0) {  // child: become /bin/echo
        execl("/bin/echo", "echo", "child_ok", static_cast<char *>(nullptr));
        std::perror("execl");  // only reached if execl failed
        _exit(127);
    }
    int status;
    if (waitpid(pid, &status, 0) == -1) {
        std::perror("waitpid");
        return 1;
    }
    if (WIFEXITED(status)) {
        std::cout << "child_status=" << WEXITSTATUS(status) << '\n';
        return 0;
    }
    std::cout << "child did not exit normally\n";
    return 1;
}
