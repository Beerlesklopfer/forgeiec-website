---
title: "Bus Configuration"
summary: "PLCopen XML schema for industrial fieldbus configuration"
---

## Namespace

```
https://forgeiec.io/v2/bus-config
```

This schema describes the ForgeIEC extension of the PLCopen XML format
for storing fieldbus configuration inside `.forge` project files.
It uses the standard-compliant `<addData>` mechanism defined by PLCopen TC6.

## Overview

The bus configuration defines the physical topology of a plant:
**Segments** (fieldbus networks) contain **Devices**, and each
device is linked to the project's I/O variables via a bus binding.

```
.forge Project
  +-- Segments (Fieldbus Networks)
  |     +-- Devices
  |           +-- Variables (via bus binding in address pool)
  +-- Address Pool (FAddressPool)
        +-- Variable: DI_1, %IX0.0, busBinding -> Maibeere
        +-- Variable: DO_1, %QX0.0, busBinding -> Maibeere
```

## XML Structure

The bus configuration is stored as `<addData>` at project level:

```xml
<project>
  <!-- Standard PLCopen content -->
  <types>...</types>
  <instances>...</instances>

  <!-- ForgeIEC bus configuration -->
  <addData>
    <data name="https://forgeiec.io/v2/bus-config"
          handleUnknown="discard">
      <fi:busConfig xmlns:fi="https://forgeiec.io/v2">

        <fi:segment id="a3f7c2e1-..."
                    protocol="modbustcp"
                    name="Fieldbus Hall 1"
                    enabled="true"
                    interface="eth0"
                    bindAddress="192.168.24.100/24"
                    gateway=""
                    pollIntervalMs="0">

          <fi:device hostname="Maibeere"
                     ipAddress="192.168.24.25"
                     port="502"
                     slaveId="1"
                     anvilGroup="Maibeere"/>

          <fi:device hostname="Stachelbeere"
                     ipAddress="192.168.24.26"
                     port="502"
                     slaveId="1"
                     anvilGroup="Stachelbeere"/>

        </fi:segment>

      </fi:busConfig>
    </data>
  </addData>
</project>
```

## Elements

### `fi:busConfig`

Root element. Contains one or more `fi:segment` elements.

| Attribute | Required | Description |
|-----------|----------|-------------|
| `xmlns:fi` | yes | Namespace: `https://forgeiec.io/v2` |

### `fi:segment`

A fieldbus segment (physical network).

| Attribute | Required | Type | Description |
|-----------|----------|------|-------------|
| `id` | yes | UUID | Unique segment identifier |
| `protocol` | yes | String | Protocol: `modbustcp`, `modbusrtu`, `ethercat`, `profibus` |
| `name` | yes | String | Display name (user-defined) |
| `enabled` | no | Bool | Segment active (`true`) or disabled (`false`). Default: `true` |
| `interface` | no | String | Network interface (e.g. `eth0`, `/dev/ttyUSB0`) |
| `bindAddress` | no | String | IP/CIDR for the interface (e.g. `192.168.24.100/24`) |
| `gateway` | no | String | Gateway address (empty = no gateway) |
| `pollIntervalMs` | no | Int | Poll interval in milliseconds (`0` = as fast as possible) |

### `fi:device`

A device within a segment.

| Attribute | Required | Type | Description |
|-----------|----------|------|-------------|
| `hostname` | yes | String | Device name (used as device ID) |
| `ipAddress` | no | String | IP address (Modbus TCP) |
| `port` | no | Int | TCP port (default: `502`) |
| `slaveId` | no | Int | Modbus slave ID |
| `anvilGroup` | no | String | Anvil IPC group for zero-copy transport |

## Variable-to-Device Binding

I/O variables are **not** listed inside the `fi:device` element.
Instead, each variable in the address pool carries a `busBinding`
attribute pointing to the device's `hostname`:

```
FLocatedVariable
  name: "DI_1"
  address: "%IX0.0"
  anvilGroup: "Maibeere"
  busBinding:
    deviceId: "Maibeere"
    modbusAddress: 0
    count: 1
```

This separation is redundancy-free: the device does not directly list
its variables, but all variables belonging to a device can be retrieved
by filtering on the binding.

## IEC Address Assignment

The IEC address of a bound variable is derived from the physical topology:

```
Segment Base + Device Offset + Register Position
```

| Address Range | Meaning | Source |
|---------------|---------|--------|
| `%IX` / `%IW` / `%ID` | Physical input | Bus binding |
| `%QX` / `%QW` / `%QD` | Physical output | Bus binding |
| `%MX` / `%MW` / `%MD` | Marker (no physical I/O) | Pool allocator |

When **binding** a variable to a device, the address changes from
`%M*` (marker) to `%I*` or `%Q*` (physical). When **unbinding**,
the variable automatically receives a free marker address.

## Supported Protocols

| Protocol | `protocol` Value | Medium | Bridge Daemon |
|----------|-----------------|--------|---------------|
| Modbus TCP | `modbustcp` | Ethernet | `tongs-modbustcp` |
| Modbus RTU | `modbusrtu` | RS-485 (serial) | `tongs-modbusrtu` |
| EtherCAT | `ethercat` | Ethernet (real-time) | `tongs-ethercat` |
| Profibus DP | `profibus` | Serial (fieldbus) | `tongs-profibus` |

## Compatibility

The `handleUnknown="discard"` attribute ensures that PLCopen-compliant
tools unfamiliar with ForgeIEC can safely ignore the bus configuration
without generating errors. Conversely, ForgeIEC reads unknown `<addData>`
blocks from other vendors and preserves them when saving.

---

<div style="text-align:center; padding: 2rem;">

**ForgeIEC Bus Configuration — Offline-capable, PLCopen-compliant, redundancy-free.**

blacksmith@forgeiec.io

</div>
