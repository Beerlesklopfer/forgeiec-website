---
title: "Bus Segments"
summary: "Configuration of a fieldbus segment (a physical network on one interface)"
---

## Overview

A **bus segment** describes **one physical network on one interface of the
PLC target** — typically an Ethernet port (`eth0`, `enp3s0`) for Modbus TCP /
EtherCAT / EtherNet-IP, or a serial port (`/dev/ttyUSB0`) for Modbus RTU /
Profibus DP. For each segment, the `anvild` daemon spawns **exactly one
bridge process** (`tongs-modbustcp`, `tongs-ethercat`, ...) that handles
the traffic to all devices in that segment.

A project can hold any number of segments — each with its own protocol,
its own interface and its own polling cadence. For example a fast EtherCAT
axis controller (`eth1`, 1 ms) and a slow Modbus TCP sensor poller (`eth0`,
100 ms) can run side-by-side in the same project.

## Fields of a segment

The struct definition lives in `editor/include/model/FBusSegmentConfig.h`.
A segment is persisted in the `.forge` project as `<fi:segment>` inside
`<fi:busConfig>` (see [Bus Configuration](../)).

### Identity + protocol

| Field | Type | Meaning |
|---|---|---|
| `segmentId` | UUID | Stable primary key — auto-generated on creation, not editable. Survives rename, protocol change and IP change. |
| `protocol` | enum | `modbustcp` / `modbusrtu` / `ethercat` / `profibus` / `ethernetip`. Determines which bridge daemon is started. |
| `name` | string | User label (e.g. `"Fieldbus Hall 1"`). Free-form, shown in the tree and in logs. |
| `enabled` | bool | On/off switch. `false` = bridge is not started, devices stay offline. Default: `true`. |

### Interface + routing

| Field | Type | Meaning |
|---|---|---|
| `interface` | string | Network interface (`eth0`, `enp3s0`, `/dev/ttyUSB0`). Passed by the bridge to the socket / serial API. |
| `bindAddress` | string (IP/CIDR) | Source IP for outgoing TCP connections, e.g. `192.168.24.100/24`. Empty = OS picks the first IP of the interface. |
| `gateway` | string (IP) | Default gateway for packets leaving the local subnet. Empty = no gateway. |
| `pollIntervalMs` | int (ms) | Bridge poll interval. `0` = as fast as possible (busy loop / real-time). Typical: `100` for Modbus TCP, `0` for EtherCAT. |

### Network settings (advanced)

These fields were added in the network-settings sprint and cover cases where
the OS defaults are not enough — typically: many parallel TCP connections
per slave, long-running TCP sessions over NAT, or several subnets on a
single NIC.

| Field | Type | Meaning |
|---|---|---|
| `subnetCidr` | string (CIDR) | Local subnet of the segment, e.g. `192.168.24.0/24`. Lets the bridge route per-device gateway overrides correctly when the bind NIC carries multiple networks. |
| `sourcePortRange` | string `"min-max"` | TCP source-port pool for outgoing connections, e.g. `30000-39999`. Empty = OS picks from the ephemeral range. Important when many parallel connections to the same slave are needed (one connection per source port). |
| `keepAliveIdleSec` | int (s) | Idle seconds before the first TCP keep-alive probe is sent. `0` = OS default. |
| `keepAliveIntervalSec` | int (s) | Spacing between keep-alive probes. `0` = OS default. |
| `keepAliveCount` | int | Number of failed probes before the connection is declared dead. `0` = OS default. |
| `maxConnections` | int | Upper bound of the connection pool. `0` = unlimited. Useful against slaves with a hard connection limit. |
| `vlanId` | int (1..4094) | 802.1Q VLAN tag for outgoing frames. `0` = untagged. |

### Protocol-specific settings

The `settings` map (key/value) holds all values that only make sense for one
specific protocol — e.g. for Modbus TCP: `port`, `timeout_ms`; for Modbus
RTU: `serial_port`, `baud_rate`, `parity`, `stop_bits`; for Profibus:
`master_address`. `log_level` and `log_file` are also kept protocol-agnostic
in this same map.

## Editing flow

In the bus tree panel both paths are equivalent — they operate on the same
field set and have the same semantic effect:

| Action | Effect |
|---|---|
| **Single-click** on a segment node | The `FPropertiesPanel` (default dock: right side) shows all fields as inline editors — changes are written into the project on `editingFinished` and mark the project dirty. |
| **Double-click** on a segment node | Opens the modal `FSegmentDialog` with the same field set, grouped into *General* / *Modbus TCP* / *Advanced Network* / *Logging*. OK commits, Cancel discards. |

## Example: Modbus TCP segment

```toml
[[bus_segments]]
segment_id     = "a3f7c2e1-7c4f-4e1a-9f9c-1a2b3c4d5e6f"
protocol       = "modbustcp"
name           = "Feldbus Halle 1"
enabled        = true
interface      = "eth0"
bind_address   = "192.168.24.100/24"
gateway        = ""
poll_interval  = 100   # ms

[bus_segments.settings]
port           = "502"
timeout_ms     = "2000"
log_level      = "info"
log_file       = "/var/log/forgeiec/halle1.log"
```

This segment starts `tongs-modbustcp` on `eth0` with source IP
`192.168.24.100`, polls all devices every 100 ms and accepts up to 2000 ms
of response time per request before a timeout error is emitted on the
status stream.

## Related topics

* [Bus configuration — schema overview](../) — XML persistence and
  PLCopen `<addData>` mechanism.
* [Bus devices](../devices/) — devices within a segment.
* [Project file format](../../file-format/) — the `.forge` XML root.
