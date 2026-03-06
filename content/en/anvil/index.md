---
title: "Anvil Technology\u00ae"
summary: "Your data is forged on our anvil"
---

## Anvil Technology\u00ae: Heart of Every Forge

In every forge, the anvil is the central workpiece — where metal is shaped,
hardened and refined. **Anvil Technology\u00ae** is the intermediate layer between the
PLC runtime and the fieldbus bridges. This is where your process data
is forged: received, transformed and distributed to the right recipients.

Anvil uses a proprietary zero-copy shared memory transport
for inter-process communication. No serialization, no copies, no compromises.

---

## Architecture

```
┌──────────────┐         ┌────────────┐         ┌──────────────────┐
│              │         │            │         │                  │
│ PLC Program  │◄───────►│  forgeiecd  │◄───────►│  Modbus Bridge   │──► Field Devices
│  (IEC Code)  │  gRPC   │  (Daemon)  │  Anvil  │  EtherCAT Bridge │──► Drives
│              │         │            │ Anvil   │  Profibus Bridge  │──► Sensors
└──────────────┘         └────────────┘         │  OPC-UA Bridge   │──► SCADA
                                                └──────────────────┘

                         ◄── Anvil ──►
                         Zero-Copy IPC
                         Shared Memory
```

Data exchange between `forgeiecd` and the protocol bridges runs through
**Anvil Technology\u00ae** — a high-performance IPC channel based on zero-copy shared memory.
Each segment gets its own communication channel.

---

## Why Anvil Technology\u00ae?

### Microsecond Latency

Conventional IPC mechanisms (pipes, sockets, message queues) copy data
between processes. Anvil eliminates every copy. The data resides in shared
memory — the receiver reads directly.

| Method | Typical Latency | Copies |
|--------|----------------|--------|
| TCP Socket | 50–200 us | 2–4 |
| Unix Socket | 10–50 us | 2 |
| **Anvil Technology\u00ae** | **< 1 us** | **0** |

### Industrial Grade

- Deterministic behavior — no dynamic memory allocation in the hot path
- Lock-free algorithms — no blocking, no deadlocks
- Publish/subscribe model — loose coupling between producer and consumer
- Automatic lifecycle management — bridges are monitored and restarted on crash

### PUBLISH/SUBSCRIBE in the IEC Program

Anvil Technology\u00ae integrates seamlessly into IEC 61131-3 programming:

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

The PUBLISH/SUBSCRIBE keywords are a ForgeIEC extension to the IEC 61131-3
standard. The compiler automatically generates the Anvil bindings.

---

## Supported Protocols

Anvil Technology\u00ae connects the PLC program to all industrial fieldbuses:

| Protocol | Bridge | Status |
|----------|--------|--------|
| **Modbus TCP** | `forgeiec-modbustcp` | Available |
| **Modbus RTU** | `forgeiec-modbusrtu` | Available |
| **EtherCAT** | `forgeiec-ethercat` | In Development |
| **Profibus DP** | `forgeiec-profibus` | In Development |
| **OPC-UA** | `forgeiec-opcua` | Planned |

Each bridge runs as an independent process. `forgeiecd` starts, monitors
and restarts bridges automatically. A bridge crash affects neither the PLC
nor other bridges.

---

## Technical Details

- **IPC Framework**: Anvil Technology\u00ae (proprietary zero-copy shared memory)
- **Architecture**: One publisher/subscriber channel per bus segment
- **Data Format**: Raw IEC variables — no serialization, no overhead
- **Platforms**: x86_64, ARM64, ARMv7 (Linux)
- **Process Model**: One bridge process per active segment

---

<div style="text-align:center; padding: 2rem;">

**Anvil Technology\u00ae — Where data is forged into control commands.**

blacksmith@forgeiec.io

</div>
