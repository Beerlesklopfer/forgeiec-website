---
title: "Bus Devices"
summary: "Configuration of a device inside a bus segment (Modbus slave, EtherCAT slave, ...)"
---

## Overview

A **bus device** is a **single device inside a segment** — typically a
Modbus TCP slave (I/O block, drive), an EtherCAT slave (servo axis, I/O
coupler), a Profibus DP slave or an EtherNet-IP adapter. For each device,
the responsible bridge maintains one logical connection, polls the
configured registers and publishes the data via the Anvil IPC group to
the PLC runtime.

A device can be **modular**: a bus coupler (slot 0) carries 1..N I/O
modules in slots 1..N. Compact devices without expansion slots have an
empty `modules` list — the variables then live directly on slot 0.

## Fields of a device

The struct definition lives in `editor/include/model/FBusSegmentConfig.h`
(next to the segment). A device is persisted in the `.forge` project as
`<fi:device>` inside `<fi:segment>` (see [Bus Configuration](../)).

### Identity + addressing

| Field | Type | Meaning |
|---|---|---|
| `deviceId` | UUID | Stable primary key — auto-generated on creation. Survives hostname rename and IP change, keeping all variable bindings stable. |
| `hostname` | string | User-visible label (`"Maibeere"`, `"Stachelbeere"`). DHCP-safe, but explicitly **not** the primary key. |
| `ipAddress` | string (IP) | IP address (Modbus TCP / EtherNet-IP). Empty for devices without an IP (EtherCAT slaves identify themselves via bus position). |
| `port` | int | TCP port. Default `502` (Modbus TCP). |
| `slaveId` | int | Modbus slave ID (1..247). Usually `1` over TCP. |
| `anvilGroup` | string | Anvil IPC group for zero-copy transport between bridge and PLC runtime. Convention: same name as `hostname`. |
| `catalogRef` | string | Optional reference into an FDD catalog entry (`"WAGO-750-352"`) describing the device. |
| `description` | string | Free-text description (`"Bewaesserungsventil Sued"`). |

### Modules (slots)

| Field | Type | Meaning |
|---|---|---|
| `modules` | list of `FBusModuleConfig` | I/O modules of the device. Slot 0 = coupler / compact device, slots 1..N = expansion modules. Per module: `slotIndex`, `catalogRef`, `name`, `baseAddress`, `settings`. |

### Per-device overrides

These fields override — only for **this** device — the corresponding values
of the segment. `0` or empty string means *inherit from segment*. In the
properties panel they sit under the *Advanced Overrides* block, usually
collapsed.

| Field | Type | Meaning |
|---|---|---|
| `mac` | string `AA:BB:CC:DD:EE:FF` | MAC address for static ARP / identity check. Protects against IP theft on DHCP devices. |
| `endianness` | enum | Word/byte order for multi-register values: `"ABCD"` (big-endian, IEC default), `"DCBA"` (word swap), `"BADC"` (byte swap), `"CDAB"` (byte + word swap). Empty = inherit from segment. |
| `timeoutOverrideMs` | int (ms) | Per-device timeout. `0` = use segment timeout. |
| `retryCount` | int | Retry count per request. `0` = segment default. |
| `connectionMode` | enum | `"always"` (keep TCP open between cycles) or `"on_demand"` (reconnect per transaction). Empty = segment / bridge default. |
| `gatewayOverride` | string (IP) | Per-device gateway when the device sits in a different subnet than the bind NIC. |

### Device-specific settings

The `settings` map (key/value) carries values that only make sense for this
device or its device type — e.g. a threshold of a drive or a preferred
function code.

## Editing flow

| Action | Effect |
|---|---|
| **Single-click** on a device node | `FPropertiesPanel` shows all fields as inline editors — General block (hostname, IP, port, slave ID, Anvil group), Override block (MAC, timeout, retries, endianness, connection mode, gateway override, description) and the status table. |
| **Double-click** on a device node | Opens the modal `FBusDeviceDialog` with the same field set. In edit mode the "Import from catalog" button is locked so that a later FDD import cannot silently overwrite existing I/O variable bindings. |

## Status variables (read-only)

At runtime each device publishes a status structure that the daemon sends
through the gRPC status stream. These values are shown in the properties
panel as a **read-only table** and are **not editable** from the UI — the
bridge writes them. From ST code they are still addressable as qualified
paths under `anvil.<seg>.<dev>.Status.*`:

| Status variable | Type | Meaning |
|---|---|---|
| `xOnline` | `BOOL` | Device currently reachable (last request answered). |
| `eState` | `INT` | State enum: 0=offline, 1=connecting, 2=online, 3=error. |
| `wErrorCount` | `WORD` | Counter of failed requests since bridge start. |
| `sLastErrorMsg` | `STRING` | Last error message (timeout, Modbus exception, ...). |

```iec
IF anvil.Halle1.Maibeere.Status.xOnline AND
   anvil.Halle1.Maibeere.Status.wErrorCount < 10 THEN
    bSensor_OK := TRUE;
END_IF;
```

## Example: WAGO 750 bus coupler with two slots

A Modbus TCP bus coupler 750-352 with one 8-DI module (750-430) on slot 1
and one 8-DO module (750-530) on slot 2:

```toml
[[bus_segments.devices]]
device_id    = "0e5d5537-e328-44e6-8214-78d529b18ebd"
hostname     = "Maibeere"
ip_address   = "192.168.24.25"
port         = 502
slave_id     = 1
anvil_group  = "Maibeere"
catalog_ref  = "WAGO-750-352"
description  = "Bus coupler hall 1, row A"

[[bus_segments.devices.modules]]
slot_index   = 0
catalog_ref  = "WAGO-750-352"
name         = "Coupler"
base_address = 0

[[bus_segments.devices.modules]]
slot_index   = 1
catalog_ref  = "WAGO-750-430"
name         = "8 DI Slot 1"
base_address = 0     # Coil 0..7

[[bus_segments.devices.modules]]
slot_index   = 2
catalog_ref  = "WAGO-750-530"
name         = "8 DO Slot 2"
base_address = 0     # Discrete Output 0..7
```

The 8 inputs appear in the address pool as `%IX0.0..%IX0.7` with
`deviceId="0e5d5537-..."`, `moduleSlot=1` and `modbusAddress=0..7`. The
8 outputs likewise with `moduleSlot=2`.

## Related topics

* [Bus segments](../segments/) — the network the device lives in.
* [Bus configuration — schema overview](../) — XML persistence.
* [Project file format](../../file-format/) — address pool and
  variable-to-device bindings.
