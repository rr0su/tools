# Syscall Analysis — mypsx

## Objective
To prove that mypsx interacts directly with the Linux kernel via system calls
while accessing process and memory information.

## Tool Used
- strace (system call tracer)

## Process Enumeration Flow
1. openat() on /proc
2. getdents64() to enumerate PID directories
3. openat() on /proc/<pid>/stat
4. read() kernel-generated process metadata
5. close() file descriptors

## Memory Map Flow
1. openat() on /proc/<pid>/maps
2. read() virtual memory areas (VMAs)
3. kernel formats internal structures into text
4. userspace parses permissions and regions

## Key Observations
- No raw memory access occurs
- No ptrace or mmap required
- Kernel exposes a controlled, read-only interface
- All data is dynamically generated per syscall

## Conclusion
mypsx performs legitimate kernel interaction using documented system calls,
demonstrating real OS-level behavior rather than static file parsing.
