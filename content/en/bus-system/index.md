---
title: "Bus System"
summary: "Industrial communication with ForgeIEC"
---

## Hierarchical Bus System Management

ForgeIEC organizes industrial communication in a CoDeSys-compatible
segment hierarchy:

```
Bus Systems
+-- Modbus TCP: Hall 1 (eth0) [enabled]
|   +-- 192.168.1.100 -- Temp Module (Slave 1)
|   |   +-- Temperature : INT (%IW0)
|   |   +-- Setpoint : INT (%QW10)
|   +-- 192.168.1.101 -- Pump (Slave 2)
+-- Modbus RTU: Lab (/dev/ttyUSB0)
+-- Unassigned (Scanner Pool)
    +-- 192.168.2.55 -- Unknown
```

## Supported Protocols

| Protocol | Medium | Application |
|----------|--------|-------------|
| **Modbus TCP** | Ethernet | Building automation, process control |
| **Modbus RTU** | RS-485 (serial) | Sensors, simple field devices |
| **EtherCAT** | Ethernet (real-time) | Motion control, fast I/O |
| **Profibus DP** | Serial (fieldbus) | Manufacturing automation |

## Automatic Address Assignment

IEC addresses (`%IX`, `%QW`, `%MD` etc.) are assigned globally without
collisions. Existing addresses in global variable lists are respected.

## Device Discovery

The integrated network scanner automatically detects Modbus-capable devices.
Discovered devices can be directly assigned to a segment.

## Change Tracking

Changes to bus variables are displayed in a clear diff dialog before being
transferred to the runtime system. The user retains full control.
