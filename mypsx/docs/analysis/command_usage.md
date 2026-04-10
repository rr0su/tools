# mypsx — Command Flexibility

This document demonstrates that `mypsx` is not a hardcoded demo tool, but a flexible inspection utility.

## Basic Invocation

```
./bin/mypsx
```

Lists visible processes and their basic metadata.

## Self-Inspection

```
./bin/mypsx -p $$
```

Analyzes the calling shell's virtual memory layout.

## Arbitrary Process Inspection

```
./bin/mypsx -p <pid>
```

Works on any accessible PID, enforcing kernel permission checks.

## Evidence-Backed Execution

Each command above has:

* Captured stdout (`docs/evidence/*.out`)
* strace logs (`docs/evidence/strace_*.log`)
* Visual screenshots (`docs/visuals/*.png`)

This proves real execution, not simulated output.

## Design Intent

* CLI handles argument parsing only
* Core logic is PID-agnostic
* Output adapts dynamically to target process

## Summary

The same binary supports:

* Enumeration
* Targeted inspection
* Self-analysis

without recompilation or configuration changes.
