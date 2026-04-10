#ifndef PROC_INFO_H
#define PROC_INFO_H

#include <stddef.h>

void print_process_info(const char *pid);
void read_state(const char *pid, char *state, size_t size);

#endif
