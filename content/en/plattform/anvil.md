---
title: "Anvil"
description: "Real-time PLC runtime with zero-copy IPC and fieldbus bridge management"
weight: 2
---

## The Anvil

In every forge, the anvil is the central piece — this is where metal is shaped,
hardened, and refined. **Anvil** is the runtime environment of the ForgeIEC
platform: the place where source code meets real-time execution.

Anvil manages the PLC scan cycle, the process images, and the data exchange
between the PLC program and the fieldbus bridges. The runtime daemon `anvild`
is the heartbeat of every ForgeIEC installation.

---

## Architecture

```
+--------------+         +------------+         +------------------+
|              |         |            |         |                  |
| PLC Program  |<------->|  anvild    |<------->|  Modbus Bridge   |--> Field devices
|  (IEC Code)  |  gRPC   |  (Daemon)  |  Anvil  |  EtherCAT Bridge |--> Drives
|              |         |            |  SHM    |  Profibus Bridge  |--> Sensors
+--------------+         +------------+         |  OPC UA Bridge   |--> SCADA
                                                +------------------+

                         <-- Anvil -->
                         Zero-Copy IPC
                         Shared Memory
```

---

## Real-Time Scan Cycle

The PLC core operates in a deterministic scan cycle:

1. **Read inputs** — acquire process image from the fieldbus bridges
2. **Execute program** — process the IEC code
3. **Write outputs** — distribute results to the bridges

The cycle runs with a configurable cycle time. Anvil guarantees
deterministic behavior without dynamic memory allocation in the hot path.

---

## Anvil Technology -- Zero-Copy IPC

The data exchange between `anvild` and the protocol bridges uses
**Anvil Technology** — a high-performance IPC channel based on
zero-copy shared memory:

- **Sub-microsecond latency** — no serialization, no copies
- **Lock-free algorithms** — no blocking, no deadlocks
- **Publish/Subscribe model** — loose coupling between producer and consumer
- **One channel per segment** — isolation between bus systems

| Method | Typical Latency | Copies |
|--------|----------------|--------|
| TCP Socket | 50-200 us | 2-4 |
| Unix Socket | 10-50 us | 2 |
| **Anvil Technology** | **< 1 us** | **0** |

---

## PUBLISH/SUBSCRIBE in the IEC Program

Anvil Technology integrates seamlessly into IEC 61131-3 programming:

```iec
VAR_GLOBAL PUBLISH 'Motors'
    K1_Mains    AT %QX0.0 : BOOL;
    K1_Speed    AT %QW10  : INT;
END_VAR

VAR_GLOBAL SUBSCRIBE 'Sensors'
    Temperature AT %IW0   : INT;
    Pressure    AT %IW2   : INT;
END_VAR
```

The PUBLISH/SUBSCRIBE keywords are a ForgeIEC extension of the
IEC 61131-3 standard. The compiler automatically generates the Anvil bindings.
In the editor, the corresponding VAR_ANVIL blocks are automatically generated
and synchronized.

---

## Bridge Management

`anvild` starts, monitors, and manages all fieldbus bridges as
subprocesses:

- **One process per segment** — isolation and independent operation
- **Automatic restart** — crashed bridges are detected and restarted
- **Configuration via TOML** — `config.toml` defines segments, devices,
  and connection parameters
- **gRPC interface** — Forge Studio controls the daemon remotely

---

## Compilation

The compilation follows a two-stage model:

1. **Workstation**: Forge Studio runs `iec2c` (IEC 61131-3 to C)
2. **Target system**: `anvild` generates a platform-specific Makefile
   and calls `make` (g++)

No compiler required on the PLC. The workstation handles the
compute-intensive work.

---

## Technical Details

| Property | Value |
|----------|-------|
| **Language** | Rust |
| **Communication** | gRPC (tonic/prost) |
| **IPC** | Anvil Technology (Zero-Copy Shared Memory) |
| **Configuration** | TOML |
| **Platforms** | x86_64, ARM64, ARMv7 (Linux) |
| **Process Model** | systemd daemon + subprocesses |

---

<div style="text-align:center; padding: 2rem;">

**Anvil — Where data is forged into control commands.**

blacksmith@forgeiec.io

</div>
