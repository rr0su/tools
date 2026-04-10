What /proc is

/proc is a virtual filesystem provided by Linux.
It is not stored on disk — it is created by the kernel on the fly.
Its purpose is to let users see information about the system and processes in a human-readable way, without needing special syscalls.
Basically, it is a window into the kernel’s internal data.

-------------------

How a process maps to /proc/<pid>

Every running process in Linux has a unique PID.
The kernel creates a directory in /proc named after this PID, like /proc/1234.
Inside that directory are files representing different aspects of the process, like its name, state, memory, and open files.
So /proc/<pid> is the kernel’s representation of that specific process, exposed safely to user programs.

------------------

Purpose of /proc/<pid>/comm

      Shows the name of the process.

      Comes directly from the kernel (task_struct->comm).

      Always trustworthy — unlike command-line arguments which can be changed.

      Tools like ps or top also use it to display process names.


-----------------


Purpose of /proc/<pid>/status

     Provides a summary of the process’s state and key info.

     Contains fields like:

                      Name: process name

                     State: running, sleeping, stopped, etc.
  
                     Pid: process ID 

                     VmSize / VmRSS: memory usage

    Gives easy-to-read info about the process without digging into memory.


------------------------


Purpose of /proc/<pid>/maps

     Shows the memory layout of the process.

    Each line represents a memory region with:
  
                               Address range (virtual memory)

                               Permissions (rwxp)

                               Which file or object is mapped (heap, stack, libraries, ELF sections)

    Helps understand where code, data, heap, and stack are located in memory.

------------------------------


Why /proc/<pid>/maps is security-critical

         Reveals stack and heap locations, which are important for understanding buffer overflows and exploits.

        Shows memory permissions (read/write/execute), so you know which areas are executable or protected (NX, RWX).

        Helps in reverse engineering: you can see how ELF segments and libraries are loaded.

        Without it, you cannot reason about vulnerabilities, ASLR, or memory access controls.
