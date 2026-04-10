#include <stdio.h>
#include <dirent.h>
#include <ctype.h>
#include <string.h>

#include "proc_enum.h"
#include "proc_info.h"

/* Strict numeric validation */
static int is_numeric(const char *s)
{
    for (; *s; s++) {
        if (!isdigit(*s))
            return 0;
    }
    return 1;
}

/*
 * Enumerate processes via /proc
 */
void list_processes(void)
{
    DIR *dir = opendir("/proc");
    if (!dir)
        return;

    struct dirent *entry;
    while ((entry = readdir(dir)) != NULL) {
        if (!is_numeric(entry->d_name))
            continue;

        print_process_info(entry->d_name);
    }

    closedir(dir);
}
