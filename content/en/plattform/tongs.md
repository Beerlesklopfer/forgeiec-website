---
title: "Tongs"
description: "Fieldbus Bridges — Modbus TCP/RTU, EtherCAT, Profibus as independent processes"
weight: 6
---

## The Tongs

The tongs reach into the fire and pull out the glowing workpiece.
**Tongs** are the fieldbus bridges of the ForgeIEC platform — they reach
into the industrial periphery and bring process data safely to the
PLC core.

---

## Supported Protocols

| Protocol | Bridge | Medium | Status |
|----------|--------|--------|--------|
| **Modbus TCP** | `tongs-modbustcp` | Ethernet | Available |
| **Modbus RTU** | `tongs-modbusrtu` | RS-485 (serial) | Available |
| **EtherCAT** | `tongs-ethercat` | Ethernet (real-time) | In Development |
| **Profibus DP** | `tongs-profibus` | Serial (fieldbus) | In Development |

---

## Architecture: One Process per Segment

Each bridge runs as an independent process. `anvild` starts, monitors,
and restarts bridges automatically. A bridge crash affects neither the
PLC core nor other bridges.

```
anvild
  |-- tongs-modbustcp --config config.toml --segment mb1
  |-- tongs-modbustcp --config config.toml --segment mb2
  |-- tongs-ethercat  --config config.toml --segment ec1
  +-- tongs-profibus  --config config.toml --segment pb1
```

Communication between `anvild` and the bridges uses Anvil Technology
(Zero-Copy Shared Memory). Each segment receives its own IPC channel.

---

## Segment Hierarchy

Tongs organizes industrial communication in a CoDeSys-compatible
hierarchy:

```
Bus Systems
+-- Modbus TCP: Hall 1 (eth0) [active]
|   +-- 192.168.1.100 -- Temperature Module (Slave 1)
|   |   +-- Temperature : INT (%IW0)   [Subscribe]
|   |   +-- Setpoint : INT (%QW10)     [Publish]
|   +-- 192.168.1.101 -- Pump (Slave 2)
+-- Modbus RTU: Lab (/dev/ttyUSB0)
+-- Unassigned (Scanner Pool)
    +-- 192.168.2.55 -- Unknown
```

---

## Device Discovery

The integrated network scanner discovers field devices automatically:

- **ICMP ping scan** — determine reachable hosts in the subnet
- **Port scan** — check Modbus port (502) and other services
- **Register scan** — read Modbus registers and identify device type
- **FDD device catalog** — match known devices by their register signatures

Discovered devices land in the scanner pool and can be assigned to a
segment via drag-and-drop.

---

## Automatic Address Assignment

IEC addresses (`%IX`, `%QW`, `%MD`, etc.) are assigned globally and
without collisions. Existing addresses in global variable lists are
taken into account. The corresponding VAR_ANVIL transport blocks are
generated automatically.

---

## Direction Model

Each variable has a clear direction:

- **in** (Subscribe/Read) — bridge reads from field device, PLC receives
- **out** (Publish/Write) — PLC sends, bridge writes to field device

There is no "inout". The bridge filters: only "in" variables are read
(Modbus FC3), only "out" variables are written (Modbus FC5/FC6/FC16).

---

## Configuration

Segments and devices are configured in `config.toml`:

```toml
[[bus_segments]]
id = "mb1"
protocol = "modbus_tcp"
enabled = true

[bus_segments.settings]
interface = "eth0"
port = 502

[[bus_segments.devices]]
name = "Temperature Module"
host = "192.168.1.100"
slave_id = 1
```

---

## Technical Details

| Property | Value |
|----------|-------|
| **Language** | Rust |
| **Modbus Crate** | tokio-modbus 0.17 |
| **IPC** | Anvil Technology (Zero-Copy Shared Memory) |
| **Process Model** | One daemon per active segment |
| **Platforms** | x86_64, ARM64, ARMv7 (Linux) |

---

<div style="text-align:center; padding: 2rem;">

**Tongs — The sure grip into the industrial periphery.**

blacksmith@forgeiec.io

</div>
