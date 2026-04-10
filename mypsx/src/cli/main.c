#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "proc_enum.h"
#include "maps.h"

#define MYPSX_VERSION "1.0"

/* Print usage information */
static void print_help(const char *prog)
{
    printf("Usage: %s [OPTIONS]\n\n", prog);
    printf("Options:\n");
    printf("  -p, --pid <pid>     Inspect memory maps of target PID\n");
    printf("  -v, --verbose       Enable verbose annotations\n");
    printf("  -h, --help          Show this help message\n");
    printf("  -V, --version       Show version information\n\n");
    printf("Default behavior:\n");
    printf("  Without options, lists running processes (PID / NAME / STATE)\n");
}

/* Print version */
static void print_version(void)
{
    printf("mypsx version %s\n", MYPSX_VERSION);
}

int main(int argc, char *argv[])
{
    pid_t target_pid = -1;

    for (int i = 1; i < argc; i++) {

        /* Help */
        if (!strcmp(argv[i], "-h") || !strcmp(argv[i], "--help")) {
            print_help(argv[0]);
            return 0;
        }

        /* Version */
        if (!strcmp(argv[i], "-V") || !strcmp(argv[i], "--version")) {
            print_version();
            return 0;
        }

        /* PID selection */
        if (!strcmp(argv[i], "-p") || !strcmp(argv[i], "--pid")) {
            if (i + 1 >= argc) {
                fprintf(stderr, "mypsx: -p requires a PID\n");
                return 1;
            }

            char *end = NULL;
            target_pid = (pid_t)strtol(argv[++i], &end, 10);

            if (*end != '\0' || target_pid <= 0) {
                fprintf(stderr, "mypsx: invalid PID\n");
                return 1;
            }
            continue;
        }

        /* Unknown option */
        fprintf(stderr, "mypsx: unknown option '%s'\n", argv[i]);
        fprintf(stderr, "Try '%s --help'\n", argv[0]);
        return 1;
    }

    /* Dispatch */
    if (target_pid > 0) {
        print_maps(target_pid);
        return 0;
    }

    /* Default: list processes */
    printf("%-6s %-28s %s\n", "PID", "NAME", "STATE");
    list_processes();
    return 0;
}
