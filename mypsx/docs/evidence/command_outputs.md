# mypsx — Evidence Log

## Default Execution

Command:
          ./mypsx



Observation:
- Enumerates running processes
- No elevated privileges required
- No kernel warnings or errors

---

## Self-Inspection (PID = $$)

Command:
          ./mypsx -p $$



Observation:
- STACK, HEAP, ELF, LIB, VDSO detected
- Permission boundaries visible (R/W/X)
- NX enforcement observable
- No RWX regions in normal execution

---

## strace — List Mode

File:
- strace_list.log

Key Evidence:
- openat() on /proc
- read() of procfs entries
- No ptrace or privileged syscalls

---

## strace — Maps Mode

File:
- strace_maps.log

Key Evidence:
- openat("/proc/<pid>/maps")
- Sequential read() of VMA entries
- Clean close()

