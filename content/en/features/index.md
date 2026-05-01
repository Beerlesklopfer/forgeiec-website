---
title: "Features"
summary: "All ForgeIEC features at a glance"
---

## All Five IEC 61131-3 Languages

One editor for all languages — seamless switching, shared variables,
unified project structure.

- **Structured Text (ST)** — Syntax highlighting, auto-completion, search & replace
- **Instruction List (IL)** — Full language support with intelligent editing
- **Function Block Diagram (FBD)** — Graphical editor with block library
- **Ladder Diagram (LD)** — Familiar representation for switching logic
- **Sequential Function Chart (SFC)** — Step sequence diagrams for process control

## Industrial Bus Systems

CoDeSys-compatible segment hierarchy with automatic device discovery.

- **Modbus TCP** — Ethernet-based communication
- **Modbus RTU** — Serial RS-485 connection
- **EtherCAT** — Real-time Ethernet fieldbus
- **Profibus DP** — Proven industrial standard
- Automatic IEC address assignment without collisions
- Network scanner for device discovery
- Diff view for changes between editor and runtime

## Real-Time Data Exchange

High-performance zero-copy data exchange between PLC programs and
external systems. PUBLISH/SUBSCRIBE directly in the IEC program.

## Live Debugging

- Watch variables in real time while the PLC is running
- Force values without production downtime
- Monitoring panel with filter function

## Per-variable safety switches

Three security-sensitive data paths leave the PLC — HMI export,
live monitoring and forcing. None of them is granted implicitly: every
single variable must be opted in explicitly, and the ST compiler
verifies the gate before emitting code.

- **HMI export** — only variables explicitly tagged as HMI-exported
  reach remote SCADA/HMI systems through the OPC UA bridge. A
  reference to a non-exported variable from ST code is rejected by
  the compiler with a hard error.
- **Live monitoring** — only variables explicitly marked as monitorable
  appear on the watch stream. The Monitor column in the variables
  panel is hidden when the global monitoring switch is off.
- **Forcing** — only variables explicitly marked as forceable can be
  overwritten from the editor. The Force column likewise follows the
  global force switch.

Global switches are a second safety layer ("nothing in Production",
"force privileges only during commissioning"); the per-variable marks
are the indispensable first layer — data leaves the PLC only where the
engineer has knowingly authorised it.

## Remote Operation

- IEC compilation on the workstation — PLC requires make, g++, libstdc++ and librt
- Encrypted upload to the target system
- User management with access control
- Automatic restart after power failure
- Support for x86_64, ARM64 and ARMv7

## Standard Library

Complete IEC standard library: counters, timers, edge detection,
type conversions and mathematical functions. Extensible with
user-defined blocks.

## Open Source

No license fees. No vendor lock-in. Runs on Linux.
