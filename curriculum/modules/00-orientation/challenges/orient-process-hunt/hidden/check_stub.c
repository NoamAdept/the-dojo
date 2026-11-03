/*
 * Tiny wrapper — runs the hidden checker. Source removed after build.
 * Compile with: cc -DCHECK_SCRIPT=\"/path/to/check.py\" -o check check_stub.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#ifndef CHECK_SCRIPT
#error "CHECK_SCRIPT must be defined at compile time"
#endif

int main(int argc, char **argv) {
    /* Always the folder ./check runs in. $ACADEMY_WORKSPACE is not used: a terminal started by
     * ./run.sh inherits the no-login folder (~/signal-dojo/challenge), not this learner's one. */
    (void)argc; (void)argv;
    execlp("python3", "python3", CHECK_SCRIPT, ".", (char *)NULL);
    perror("failed to start checker");
    return 1;
}
