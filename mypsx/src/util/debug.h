#ifndef DEBUG_H
#define DEBUG_H

#include <stdio.h>
#include <stdlib.h>

/*
 * Debug macro controlled via MYPSX_DEBUG environment variable
 *
 * Usage:
 *   DEBUG("opening maps file: %s", path);
 */
#define DEBUG(fmt, ...)                             \
    do {                                            \
        if (getenv("MYPSX_DEBUG"))                  \
            fprintf(stderr, "[DEBUG] " fmt "\n", ##__VA_ARGS__); \
    } while (0)

#endif
