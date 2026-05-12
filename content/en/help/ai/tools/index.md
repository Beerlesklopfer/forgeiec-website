---
title: "What the AI can do"
summary: "Which actions the AI assistant can perform in ForgeIEC Studio — overview in plain terms"
---

## Reading and understanding — always allowed

These actions the assistant can **always** perform without enabling
anything:

- **Project overview** — name, POU count, variable count
- **List POUs** — all programs + function blocks + functions
- **Read a POU** — view the ST code of a single POU
- **List variables** — all pool variables with addresses + types,
  filtered by scope (globals, POU locals, Bellows export, …)
- **Bus configuration** — segments, devices, variable mapping
- **Aliases** — all defined variable names + addresses
- **Library** — all standard FB blocks (TON, CTU, R_TRIG, …) with
  parameters and ST examples

With this the assistant can **get to know your codebase** before
making suggestions.

---

## Live observation — always allowed

When the PLC is running, the assistant can query live values:

- **Live snapshot** — read all watched variables at once
- **Single value** — query a specific address
- **PLC status** — is it running, how much watch traffic, last
  upload
- **Cycle statistics** — task time, jitter, min/max/average
- **PLC code state** — Run / Pause / Stop
- **Start/stop recording** — live values for later analysis
- **Oscilloscope capture** — time series of one or more addresses,
  with optional trigger (edge, threshold)

With this the assistant can do **diagnostics**: "Why does
`Motor_Ready` not switch? Look at the last 5 seconds on the
oscilloscope."

---

## Changes — only in the unlocked version

The following actions change your project or the PLC. They are
**switched off in the default build from the internet** and require
a special version with `MCP_OVERRIDE_SECURITIES=ON`. Every action
asks back first:

### Project changes

- **Create variable** — new pool variable with address + type
- **Rename or move variable** — between POU-local, globals,
  Bellows export
- **Delete variable** — carefully
- **Create POU** — new program, function block or function
- **Rename POU** — Tree-sitter-based (backend refactor follows)
- **Delete POU** — carefully, task bindings may become dangling
- **Set POU body** — replace the ST code
- **Set flag** — Bellows export, retain, constant, monitor-enable

### Compile + deploy

- **Pre-compile check** — fast syntax check without g++
- **Full compile** — like the build button in the toolbar
- **Generate code** — view the generated C files (without deploy)
- **Deploy** — compile, upload, restart the PLC binary
- **Deploy status** — phases + g++ stderr from the last deploy

### PLC control

- **Start** — PLC run command
- **Stop** — PLC stop command, outputs go to safe state
- **Pause / Resume** — halt cycle without complete stop
- **Force** — pin a variable (ONLY via the GUI, **not** via the AI;
  see [Security model](/help/ai/security/))

---

## Tasks + task management

The assistant can also change the task setup:

- **List resources** + **list tasks** in a resource
- **Read program instances** of a task
- **Create new task** with cycle time + priority
- **Place program instance on task**
- **Cycle overview** across all tasks

---

## Assistant queries itself

When the AI does not know what a certain tool does, it can query
**its own help**:

- `forge.help` — cheat sheet of all available actions with short
  descriptions, grouped by family
- `forge.help_for(name)` — detailed manual for a specific tool,
  with examples and error classes

With this a fresh model after a restart can **reorient itself**
without you having to explain how ForgeIEC works.

---

## Anvil / Bellows / HMI connection

The assistant can also address the HMI bridge (Bellows) and the
SHM IPC layer (Anvil):

- **List Bellows groups + variables** and read them
- **List Anvil topics** + read them
- **Anvil plugin status** + health check
- **Modbus bridge status** (tongs-modbustcp)

This is diagnostic material when the HMI sees something different
from the PLC.

---

## Editor operation

A handful of editor actions are also reachable via the AI:

- **Quit ForgeIEC Studio** — clean stop without kill -9
- **Recent ForgeIEC Studio logs** — what ForgeIEC Studio itself logged
- **Fetch / answer confirmations**
- **List pending confirmations**

---

## Next

- [Personas](/help/ai/agents/) — which character can do which of
  the above actions
- [Security model](/help/ai/security/) — why which action is gated
- [Back to the AI overview](/help/ai/)
