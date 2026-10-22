---
title: "Features"
summary: "All ForgeIEC features at a glance"
---

## IEC 61131-3: ST today, the other four in progress

Structured Text is in productive use (pilot operation); the editors
for the other four languages are in progress and do not compile yet.

- **Structured Text (ST)** {{< status "use" >}} — syntax highlighting, auto-completion, search & replace; own compiler core with object-oriented extensions
- **Instruction List (IL)** {{< status "wip" >}}
- **Function Block Diagram (FBD)** {{< status "wip" >}} — graphical editor with block library
- **Ladder Diagram (LD)** {{< status "wip" >}} — familiar representation for switching logic
- **Sequential Function Chart (SFC)** {{< status "wip" >}} — step sequence diagrams for process control

## Industrial Bus Systems

Familiar segment hierarchy from established IEC-61131-3 IDEs, with automatic device discovery.

- **Modbus TCP** {{< status "use" "available" >}} — Ethernet-based communication
- **Modbus RTU** {{< status "use" "available" >}} — serial RS-485 connection
- **LoRaWAN** {{< status "wip" "in progress (focus)" >}} — wireless sensors for agriculture and wide-area plants
- **EtherCAT** {{< status "wip" "skeleton, in progress" >}} — real-time Ethernet fieldbus
- **PROFIBUS DP** {{< status "wip" "skeleton, in progress" >}} — proven industrial standard
- **EtherNet/IP** {{< status "wip" "skeleton, in progress" >}}
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
  reach external systems. A
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
- Support for x86_64, ARM64 and ARMv7 (armhf: runtime and Hearth)

## Standard Library

Complete IEC standard library: counters, timers, edge detection,
type conversions and mathematical functions. Extensible with
user-defined blocks.

## Licence

No runtime licence per controller, no vendor lock-in. The tools and
services are licensed under AGPL-3.0-or-later; the generated control
code, the runtime API headers and libanvil under Apache-2.0. A
commercial licence is available. Runs on Linux; a Windows build of
the Studio exists (installer on request).
