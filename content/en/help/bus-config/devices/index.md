---
title: "Bus devices"
summary: "Configuration of a device inside a bus segment — FDD integration, modules, status variables, per-device overrides"
---

{{< components "studio,tongs,anvild" >}}

## What is a device?

A **bus device** is **a single device inside a segment** — Modbus
TCP slave (I/O block, drive), EtherCAT slave (servo axis, I/O
coupler), Profibus DP slave or EtherNet/IP adapter. The bridge
daemon maintains one logical connection per device, polls the
configured registers and publishes the data via **Anvil zero-copy
IPC** to the PLC runtime.

A device can be **modular**: a bus coupler (slot 0) carries 1..N
I/O modules in slots 1..N. Compact devices without expansion
slots have an empty `modules` list — variables then sit at slot 0.

---

## FDD integration

Instead of describing every device manually, you **import a
manufacturer FDD** at creation. ForgeIEC Studio:

1. Reads `<Identification>`, `<DiagnosticDecode>`,
   `<ModuleProtocol>`, `<Document>` from the FDD
2. Shows the **embedded PDF data sheet** in the documents tab of
   the properties panel
3. Populates **status variables** from the diagnostic-bit
   definitions
4. Filters the **module picker** to show only compatible modules
   (matched via `<ModuleProtocol>`)

The `catalogRef` field of the device points to the FDD used. You
can swap an FDD (e.g. `weidmueller/UR20-FBC-PN-IRT-V2` → `-V3`)
and keep all I/O variable bindings — identity hangs on the
`deviceId` UUID, not the manufacturer entry.

Create your own FDDs via `File → New FDD` (diagnostics tab +
documents tab in the FDD editor).

More on the FDD system: [news post](/news/catalog-fdd/).

---

## Device fields

The struct definition lives in
`editor/include/model/FBusSegmentConfig.h`. A device is persisted
in the `.forge` project as `<fi:device>` under `<fi:segment>`
(see [bus configuration](../)).

### Identity + addressing

| Field | Type | Meaning |
|---|---|---|
| `deviceId` | UUID | Stable primary key — generated on creation, survives hostname rename and IP change. Keeps all variable bindings stable. |
| `hostname` | String | User-visible label (`"Stachelbeere"`, `"Maibeere"`). **Is** part of the IEC namespace (`anvil.<Segment>.Stachelbeere.<...>`). DHCP-safe, but **not** a primary key. |
| `ipAddress` | String (IP) | IP address (Modbus TCP / EtherNet/IP). Empty for devices without an IP (EtherCAT slaves identify via bus position). |
| `port` | Int | TCP port. Default `502` (Modbus TCP). |
| `slaveId` | Int | Modbus slave ID (1..247). For TCP usually `1`. |
| `catalogRef` | String | Reference to the FDD catalog entry, e.g. `"weidmueller/UR20-FBC-PN-IRT-V2"`. Drives the module picker + diagnostic-bit resolution. |
| `description` | String | Free text (`"Irrigation valve south"`). |

### Modules (slots)

| Field | Type | Meaning |
|---|---|---|
| `modules` | List of `FBusModuleConfig` | I/O modules of the device. Slot 0 = coupler / compact device, slots 1..N = expansion modules. Per module: `slotIndex`, `catalogRef`, `name`, `baseAddress`, `settings`. |

For modular couplers, each module ships with its own FDD file —
again with diagnostic bits + data sheet. The picker shows only
modules that the coupler understands according to its
`<ModuleProtocol>`.

### Per-device overrides

Override — for **this** device only — the corresponding values
of the segment. `0` or empty string means *inherit from segment*.
In the properties panel usually collapsed under *Advanced
Overrides*.

| Field | Type | Meaning |
|---|---|---|
| `mac` | String `AA:BB:CC:DD:EE:FF` | MAC address for static ARP / identity check. Protects against IP hijacking for DHCP devices. |
| `endianness` | Enum | `"ABCD"` (big-endian, IEC default), `"DCBA"` (word swap), `"BADC"` (byte swap), `"CDAB"` (both). Empty = inherit from segment. |
| `timeoutOverrideMs` | Int (ms) | Per-device timeout. `0` = segment timeout. |
| `retryCount` | Int | Retries per request. `0` = segment default. |
| `connectionMode` | Enum | `"always"` (keep TCP open) or `"on_demand"` (reconnect per transaction). Empty = segment default. |
| `gatewayOverride` | String (IP) | Own gateway if the device is in a different subnet than the bind NIC. |

### Device-specific settings

The `settings` map (key/value) carries values that only make sense
for this device or its device type — e.g. a frequency-converter
threshold or a preferred Modbus function code.

---

## Edit path in ForgeIEC Studio

| Action | Effect |
|---|---|
| **Single click** on a device node | `FPropertiesPanel` shows all fields as inline editors — general, override block, diagnostic bits with live values, status table. |
| **Double click** | Modal dialog `FBusDeviceDialog`. In edit mode the "Import from catalog" button is locked so that a later FDD import does not overwrite existing I/O bindings. |

---

## Status variables (read-only)

Every device publishes a status struct at runtime. Properties
panel shows them as a **read-only table** — the bridge writes
them, the ST code reads them. On the ST side, they are accessible
under `anvil.<Segment>.<Device>.Status.<Var>`:

| Status variable | Type | Meaning |
|---|---|---|
| `xOnline` | `BOOL` | Device currently reachable (last request was answered) |
| `eState` | `INT` | State enum: 0=offline, 1=connecting, 2=online, 3=error |
| `wErrorCount` | `WORD` | Failed requests since bridge start |
| `sLastErrorMsg` | `STRING` | Last error message (timeout, Modbus exception, ...) |

Additionally, all bits from the **FDD `<DiagnosticDecode>`**
section appear as type-safe status members — e.g. `WireBreak`,
`ShortCircuit`, `OverTemperature`. Properties panel shows meaning
+ severity multilingually (DE/EN) from the FDD.

ST example:

```text
IF anvil.Halle1.Maibeere.Status.xOnline AND
   anvil.Halle1.Maibeere.Status.wErrorCount < 10 AND
   NOT anvil.Halle1.Maibeere.Status.WireBreak THEN
    bSensor_OK := TRUE;
END_IF;
```

AI-assistant diagnostic loop via MCP `catalog.diag_bits` returns
the resolved meaning of these bits in plain text.

---

## Example: Weidmueller UR20 coupler with two modules

A ProfiNet IRT coupler (UR20-FBC-PN-IRT-V2) with an 8-DI module
and an 8-DO module:

```toml
[[bus_segments.devices]]
device_id    = "0e5d5537-e328-44e6-8214-78d529b18ebd"
hostname     = "Stachelbeere"
ip_address   = "192.168.24.25"
port         = 502
slave_id     = 1
catalog_ref  = "weidmueller/UR20-FBC-PN-IRT-V2"
description  = "Bus coupler hall 1, row A"

[[bus_segments.devices.modules]]
slot_index   = 0
catalog_ref  = "weidmueller/UR20-FBC-PN-IRT-V2"
name         = "Coupler"
base_address = 0

[[bus_segments.devices.modules]]
slot_index   = 1
catalog_ref  = "weidmueller/UR20-8DI-P"
name         = "8 DI slot 1"
base_address = 0

[[bus_segments.devices.modules]]
slot_index   = 2
catalog_ref  = "weidmueller/UR20-8DO-P"
name         = "8 DO slot 2"
base_address = 0
```

Effect:

- The 8 inputs appear in the address pool as `%IX0.0..%IX0.7`
  with `deviceId=0e5d5537-...`, `moduleSlot=1`, `modbusAddress=0..7`
- The 8 outputs similarly with `moduleSlot=2`
- ST access: `anvil.Halle1.Stachelbeere.IO.DI_1` /
  `anvil.Halle1.Stachelbeere.IO.DO_1`
- Diagnostic bits from the FDD: `Status.WireBreak`,
  `Status.ShortCircuit`, etc. — type-safe, multilingual
  descriptions

---

## See also

- [Bus segments](../segments/) — the network the device lives in
- [Bus configuration — schema overview](../) — 5-level namespace,
  XML persistence
- [Catalog + FDD system](/news/catalog-fdd/) — manufacturer data
  + diagnostic-bit resolver
- [Tongs bridge family](/news/tongs-bridges/) — fault model
