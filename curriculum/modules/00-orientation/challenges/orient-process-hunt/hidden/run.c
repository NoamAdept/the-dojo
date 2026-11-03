/*
 * ./run — starts a background helper. Source is removed after build.
 */
#define _POSIX_C_SOURCE 200809L
#include <dirent.h>
#include <errno.h>
#include <fcntl.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <time.h>
#include <unistd.h>

static void die(const char *msg) {
    fprintf(stderr, "run failed: %s\n", msg);
    exit(1);
}

static int work_mode(void) {
    for (;;) sleep(30);
    return 0;
}

static void resolve_self(char *out, size_t out_sz, char *argv0) {
#if defined(__APPLE__)
    if (argv0 && argv0[0] == '/') {
        strncpy(out, argv0, out_sz - 1);
        out[out_sz - 1] = '\0';
        return;
    }
    if (argv0 && strchr(argv0, '/')) {
        if (getcwd(out, out_sz) == NULL) die("getcwd");
        size_t len = strlen(out);
        if (len + 1 + strlen(argv0) >= out_sz) die("path too long");
        out[len] = '/';
        memcpy(out + len + 1, argv0, strlen(argv0) + 1);
        return;
    }
#endif
    ssize_t n = readlink("/proc/self/exe", out, out_sz - 1);
    if (n > 0) {
        out[n] = '\0';
        return;
    }
    if (!argv0 || !argv0[0]) die("cannot resolve self");
    if (argv0[0] == '/') {
        strncpy(out, argv0, out_sz - 1);
        out[out_sz - 1] = '\0';
        return;
    }
    if (getcwd(out, out_sz) == NULL) die("getcwd");
    size_t len = strlen(out);
    if (len + 1 + strlen(argv0) >= out_sz) die("path too long");
    out[len] = '/';
    memcpy(out + len + 1, argv0, strlen(argv0) + 1);
}

/* Stop only the helpers this ./run started before (same program file, so the same challenge
 * folder). On a classroom server every learner runs as the same OS account, so a plain
 * `pkill -f 'helper --work'` would also kill the other learners' helpers. */
static void stop_my_helpers(const char *self) {
#if defined(__linux__)
    DIR *d = opendir("/proc");
    if (!d) return;
    struct dirent *e;
    char path[64], exe[4096], cmd[16];
    size_t self_len = strlen(self);
    while ((e = readdir(d)) != NULL) {
        char *end;
        long pid = strtol(e->d_name, &end, 10);
        if (*end || pid <= 0 || pid == (long)getpid()) continue;
        snprintf(path, sizeof(path), "/proc/%ld/exe", pid);
        ssize_t n = readlink(path, exe, sizeof(exe) - 1);
        if (n <= 0) continue;
        exe[n] = '\0';
        /* Start rebuilds ./run, so an older helper's exe reads "<path> (deleted)". */
        if (strncmp(exe, self, self_len) != 0 || (exe[self_len] && strcmp(exe + self_len, " (deleted)") != 0))
            continue;
        snprintf(path, sizeof(path), "/proc/%ld/cmdline", pid);
        FILE *f = fopen(path, "r");
        if (!f) continue;
        size_t got = fread(cmd, 1, sizeof(cmd) - 1, f);
        fclose(f);
        cmd[got] = '\0';
        if (strcmp(cmd, "helper") == 0) kill((pid_t)pid, SIGTERM);
    }
    closedir(d);
#else
    (void)self;
    int reap = system("pkill -f 'helper --work' >/dev/null 2>&1");
    (void)reap;
#endif
}

int main(int argc, char **argv) {
    if (argc >= 2 && strcmp(argv[1], "--work") == 0) {
        return work_mode();
    }

    char base[512], note_path[576], code[64], self[4096];
    unsigned rnd;
    pid_t pid;

    resolve_self(self, sizeof(self), argv[0]);
    stop_my_helpers(self);
    {
        struct timespec ts = {.tv_sec = 0, .tv_nsec = 150000000L};
        nanosleep(&ts, NULL);
    }

    rnd = ((unsigned)time(NULL) ^ (unsigned)getpid() * 2654435761u);
    snprintf(base, sizeof(base), "/tmp/academy_note_%u", rnd % 100000000u);
    if (mkdir(base, 0700) != 0 && errno != EEXIST) die("mkdir");
    snprintf(note_path, sizeof(note_path), "%s/note.txt", base);
    snprintf(code, sizeof(code), "CODE-%08X", rnd);

    FILE *f = fopen(note_path, "w");
    if (!f) die("note");
    fprintf(
        f,
        "This is a small notes file created by the helper program.\n"
        "secret_code=%s\n",
        code
    );
    fclose(f);

    pid = fork();
    if (pid < 0) die("fork");
    if (pid == 0) {
        if (setsid() < 0) _exit(1);
        int nullfd = open("/dev/null", O_RDWR);
        if (nullfd >= 0) {
            dup2(nullfd, 0);
            dup2(nullfd, 1);
            dup2(nullfd, 2);
            if (nullfd > 2) close(nullfd);
        }
        execl(self, "helper", "--work", "--notes", note_path, (char *)NULL);
        _exit(127);
    }

    printf("Helper program started in the background.\n");
    printf("It did not print a process number. Go find it.\n");
    return 0;
}
