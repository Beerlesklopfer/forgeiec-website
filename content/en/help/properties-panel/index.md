---
title: "Properties Panel"
summary: "Inline editor for the bus element selected in the project tree"
---

## Overview

The **Properties panel** is the right-hand detail view of the editor's
main window. It shows **every field of the element currently selected
in the project tree** and makes those fields editable inline — no need
to open a modal dialog for each edit.

```
Project tree                          Properties panel
+-- Bus                               +-- Name:        OG-Modbus
|   +-- segment_modbus    <-- click   |   Protocol:    [modbustcp ▼]
|       +-- device_motor              |   Interface:   eth0
|           +-- slot_0                |   Bind Addr:   192.168.1.10/24
+-- Programs                          |   Poll:        100 ms
|   +-- PLC_PRG                       |   Enabled:     [x]
                                      |   Port:        502
                                      |   Timeout:     2000 ms
```

A **single click** on a tree node immediately renders the matching
field list — a **double click** additionally opens the modal
configuration dialog ([Bus configuration](../bus-config/)) with the
exact same field set.

The panel is wrapped in a `QScrollArea` and scrolls vertically: devices
with FDD extensions plus the status table easily reach 40+ fields, and
all of them must stay reachable even when the dock is narrow.

## Bus segment

When a bus segment is selected, the panel shows:

| Field | Meaning |
|---|---|
| **Name** | Display name in the project tree. |
| **Protocol** | `modbustcp`, `modbusrtu`, `ethercat`, `profibus`, `ethernetip`. |
| **Interface** | Network interface the bridge binds to (`eth0`, `eth1`, …). |
| **Bind Address** | CIDR notation, e.g. `192.168.1.10/24`. Validated. |
| **Gateway** | Default gateway for the bridge process. |
| **Poll Interval** | Period in `ms` at which the bridge polls its devices. |
| **Enabled** | Whether the bridge subprocess is active. |

### Advanced Network (all optional)

Mirrors the same group in `FSegmentDialog` and overrides OS / bridge
defaults:

  - **Subnet CIDR** (`192.168.24.0/24`)
  - **Source Port Range** (`30000-39999`)
  - **Keep-Alive Idle / Interval / Count** (TCP heartbeat)
  - **Max Connections** (`0` = unlimited)
  - **VLAN ID** (`0` = untagged)

### Protocol-specific

| Protocol | Fields |
|---|---|
| `modbustcp`  | `Port` (default `502`), `Timeout` in `ms` (default `2000`). |
| `modbusrtu`  | `Serial Port` (e.g. `/dev/ttyUSB0`), `Baud Rate`, `Parity` (`none`/`even`/`odd`). |
| `profibus`   | `Serial Port`, `Baud Rate` (up to 12 Mbit/s), `Master Address` (0..126). |

### Logging

  - **Log Level** — `off` / `error` / `warn` / `info` / `debug`.
  - **Log File** — e.g. `/var/log/forgeiec/segment.log`. Empty = stdout.

## Bus device

| Field | Meaning |
|---|---|
| **Hostname** | DNS or display name. |
| **IP Address** | IPv4 of the device. |
| **Port** | Modbus port on the slave (default `502`). |
| **Slave ID** | Modbus unit ID (0..247). |
| **Anvil Group** | Anvil IPC group name — also the name of the auto-generated `AnvilVarList`. Renaming it synchronously renames the GVL tag, the AnvilVarList and every pool variable with `anvilGroup = oldGroup`. |

### Advanced overrides (all optional, empty = inherit from segment)

  - **MAC Address** — `AA:BB:CC:DD:EE:FF`. Validated.
  - **Endianness** — `ABCD` / `DCBA` / `BADC` / `CDAB`.
  - **Timeout** in `ms`. `0` = inherit from segment.
  - **Retry Count**. `0` = inherit from segment.
  - **Connection Mode** — `always connected` or `on demand`.
  - **Gateway (override)** — only when the device lives in a different subnet.
  - **Description** — free text (e.g. `South irrigation valve`).

### Status variables (read-only)

Every device automatically exposes the common fault model — seven
implicit fields published as a read-only status topic over Anvil:

| Name | IEC type | Meaning |
|---|---|---|
| `xOnline`              | `BOOL`         | TRUE when `eState = Online` or `Degraded`. |
| `eState`               | `eDeviceState` | Current fault state. |
| `wErrorCount`          | `UDINT`        | Total errors since the bridge started. |
| `wConsecutiveFailures` | `UDINT`        | Failures since last `Online` (resets on `Online`). |
| `wLastErrorCode`       | `UINT`         | `0` = none; `1..99` common; `100+` protocol-specific. |
| `sLastErrorMsg`        | `STRING[48]`   | UTF-8, zero-padded. |
| `tLastTransition`      | `ULINT`        | Unix time (ms) of the last state transition. |

When the device is bound to an **FDD** (field device description) via
`catalogRef`, the status table additionally lists the FDD-defined
extensions, marked `FDD +<offset>` in the `Source` column.

In ST code every status variable is reachable as
`anvil.<seg>.<dev>.Status.*`:

```iec
IF NOT anvil.OG_Modbus.K1_Mains.Status.xOnline THEN
    Lampe_Stoerung := TRUE;
END_IF;
```

## Bus module

Bus modules are I/O slices inside a device. The panel shows:

### Metadata

  - **Module** (display name or `catalogRef`)
  - **Slot** (slot index within the device)
  - **Catalog** (FDD reference, e.g. `Beckhoff.EL2008`)
  - **Base Addr** (IEC base offset)

### IO variables table

Lists every pool variable whose `busBinding.deviceId` and
`busBinding.moduleSlot` match this module. Columns:

| Column | Content |
|---|---|
| **Name** | Pool name (editable, e.g. `Motor_Run`). |
| **Type** | IEC type (editable, e.g. `BOOL`, `INT`). |
| **Address** | IEC address (`%IX0.0`, read-only). |
| **Bus Addr** | Modbus register offset (read-only). |
| **Dir** | `in` or `out` (read-only). |

Sort order: inputs before outputs, then ascending by bus address.

## Edit behaviour

Every edit in the panel runs straight against the model:

  1. Edit on the widget (`editingFinished` / `valueChanged` / `toggled`).
  2. The model field is updated (`seg->name = ...`).
  3. `project->markDirty()` raises the dirty flag.
  4. The `busConfigEdited` signal is emitted.
  5. The main window refreshes the project tree label if needed.

There is **no** explicit `Apply` and **no** `Cancel` — edits take
effect immediately. `Ctrl+Z` (undo) on the project tree reverts the
last edit.

## Related topics

  - [Bus configuration](../bus-config/) — modal dialogs with the same
    field set, for power users with high edit volume.
  - [Variables panel](../variables/) — the pool that feeds the
    `IO variables` table.
