# Attack Surface Implications

**Command:** `mypsx`  
**Purpose:** Enumerates processes and memory maps of processes (`/proc/[pid]/maps`).  

## Key Observations
| Feature | Security Implication | Notes |
|---------|-------------------|------|
| Process enumeration (`--all`) | Read-only access; low risk | Does not modify kernel state |
| Memory map inspection (`--pid <pid>`) | Could expose memory layout | Requires appropriate permissions; mitigated by Linux UID/GID access control |
| CLI flags (`--all`, `--pid`) | Predictable behavior | Minimal user input; low risk of injection |

**Conclusion:**  
`mypsx` is a read-only utility. It exposes memory layout but follows OS permissions, limiting attack surface. No write or exec operations are performed.  

**Screenshots / Evidence:**  
- Default execution: `docs/visuals/mypsx_default.png`  
- Memory map output: `docs/visuals/mypsx_self_map_top.png`
