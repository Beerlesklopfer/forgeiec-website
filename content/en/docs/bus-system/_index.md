---
title: "Bus System"
linkTitle: "Bus System"
weight: 3
description: Configure Modbus TCP/RTU, EtherCAT, and Profibus DP bus segments.
---

## Overview

ForgeIEC uses a CoDeSys-style hierarchical bus system:

```
Bus Systems
├── Modbus TCP: Hall 1 (eth0) [enabled]
│   ├── 192.168.1.100 — Temp Module (Slave 1)
│   │   ├── Temperature : INT (%IW0, Addr 0)
│   │   └── Setpoint : INT (%QW10, Addr 10)
│   └── 192.168.1.101 — Pump (Slave 2)
├── Modbus TCP: Lab (eth1) [disabled]
└── Unassigned (Scanner Pool)
    └── 192.168.2.55 — Unknown
```

## Segments

A segment defines a bus protocol and network interface:

- **Modbus TCP**: Ethernet-based, one connector per segment
- **Modbus RTU**: Serial (RS-485), baud rate and parity settings
- **EtherCAT**: Real-time Ethernet fieldbus
- **Profibus DP**: Industrial serial fieldbus

## Devices

Each device belongs to a segment and has:

- **IP Address / Serial Address**: Network endpoint
- **Slave ID**: Modbus unit identifier
- **I/O Variables**: Mapped to IEC addresses and Modbus registers

## Auto-Addressing

ForgeIEC automatically assigns IEC addresses (`%IX`, `%QW`, etc.) to bus
variables. Addresses are assigned sequentially per category, starting after
any addresses already used by regular Global Variable Lists.

## VAR_DEL Synchronization

Bus variables are stored as IceOryx VAR_DEL POUs (PUBLISH/SUBSCRIBE).
Changes between the local project and the runtime server are shown in a
diff dialog before synchronization.

Direction mapping:
- **In** (Subscribe): Read from device → PLC
- **Out** (Publish): PLC → Write to device
- **InOut**: Both directions (appears in PUBLISH and SUBSCRIBE blocks)
