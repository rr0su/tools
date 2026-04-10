#ifndef MAPS_H
#define MAPS_H

#include <sys/types.h>

/*
 * print_maps()
 *
 * Kernel-aware virtual memory analyzer.
 * Reports:
 *  - Virtual Memory Areas (VMAs)
 *  - Permission model (RW / X / NX)
 *  - Region classification (STACK, HEAP, ELF, LIB, ANON)
 *  - Segment role inference (.text, .data, .rodata)
 *
 * Physical memory addresses are intentionally not exposed.
 */
void print_maps(pid_t pid);

#endif
