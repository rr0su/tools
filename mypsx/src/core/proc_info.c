#include <stdio.h>
#include <string.h>

#include "proc_info.h"

/*
 * Read process state from /proc/<pid>/stat
 */
void read_state(const char *pid, char *state, size_t size)
{
    (void)size;

    char path[64];
    snprintf(path, sizeof(path), "/proc/%s/stat", pid);

    FILE *fp = fopen(path, "r");
    if (!fp) {
        strcpy(state, "?");
        return;
    }

    int dummy;
    char comm[256];
    char st;

    fscanf(fp, "%d %255s %c", &dummy, comm, &st);
    fclose(fp);

    state[0] = st;
    state[1] = '\0';
}

/*
 * Print one process entry
 */
void print_process_info(const char *pid)
{
    char name[256] = "?";
    char state[8]  = "?";

    char path[64];
    snprintf(path, sizeof(path), "/proc/%s/comm", pid);

    FILE *fp = fopen(path, "r");
    if (fp) {
        fgets(name, sizeof(name), fp);
        name[strcspn(name, "\n")] = '\0';
        fclose(fp);
    }

    read_state(pid, state, sizeof(state));

    printf("%-6s %-28s %s\n", pid, name, state);
}
