mypsx

A Linux process virtual memory inspection tool focused on kernel‑exposed VMAs and security implications.

This tool is not a memory dumper.
It exists to help reason about what the kernel exposes, what it protects, and what that means for exploitation and defense.

Why this exists

Linux exposes process memory layout through procfs.
Most tools either ignore it or treat it as raw text.

mypsx turns /proc/<pid>/maps into structured, security‑relevant insight:

what regions exist,

how they are protected,

and what constraints those protections impose.

What it inspects (kernel perspective)

mypsx reads kernel‑managed Virtual Memory Areas (VMAs) and enriches them with meaning:

STACK

HEAP

ELF segments

Shared libraries

VDSO / VVAR

Anonymous mappings

For each VMA it analyzes:

permissions (R / W / X)

NX enforcement

executable boundaries

backing objects

This reflects what the kernel allows, not guesses from user space.

Architecture overview

The project is intentionally split by responsibility:

src/core/
Core logic: proc parsing, VMA classification, security analysis

src/cli/
Argument handling and dispatch only

src/util/
Header‑only debug and helpers

bin/
Final compiled binary (no source mixed with artifacts)

docs/
Architecture notes, analysis, evidence, and visuals

This separation keeps parsing, analysis, and presentation independent.

Security relevance

mypsx highlights properties that directly affect exploit feasibility:

NX enforcement
Writable regions should not be executable

RWX detection
RWX VMAs are flagged as dangerous misconfigurations

Stack / Heap protections
NX on stack and heap blocks classic shellcode injection

ASLR visibility
Non‑contiguous VMAs indicate address randomization

The output is meant to support reasoning, not exploitation.

Build & usage

Build (reproducible):

./scripts/build.sh


Run:

./bin/mypsx


Inspect a specific process:

./bin/mypsx -p <pid>


Self‑inspection example:

./bin/mypsx -p $$

Evidence

All evidence is frozen and reproducible:

Command outputs: docs/evidence/

strace logs proving procfs access

Screenshots for visual confirmation: docs/visuals/

No privileged syscalls.
No ptrace.
No memory modification.

Limitations & future work

This tool intentionally limits scope.

Register state (RIP / RSP / RBP) is not accessible via maps

Segment roles are inferred heuristically

No kernel‑space visibility

No live exploit detection

See:

docs/limitations.md

docs/future_work.md

Example output

Below is a real execution against the running shell process:
