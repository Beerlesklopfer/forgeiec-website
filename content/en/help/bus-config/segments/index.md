---
title: "Bus segments"
summary: "Fields per segment, bridge lifecycle, protocol-specific settings"
---

{{< components "studio,tongs,anvild" >}}

## What is a segment?

A **bus segment** is **one physical network on one interface of
the PLC target** — Ethernet port (`eth0`, `enp3s0`) for Modbus
TCP / EtherCAT / EtherNet-IP, serial port (`/dev/ttyUSB0`) for
Modbus RTU / Profibus DP.

For each segment, `anvild` starts **exactly one bridge daemon**
(`tongs-modbustcp`, `tongs-ethercat`, ...). It handles traffic to
all devices in the segment.

A project can hold any number of segments — each with its own
protocol, interface and polling rate. A fast EtherCAT axis control
(`eth1`, 1 ms) + a slow Modbus TCP sensor acquisition (`eth0`,
100 ms) run in parallel in the same project.

---

## Segment fields

The struct definition lives in
`editor/include/model/FBusSegmentConfig.h`. A segment is persisted
in the `.forge` project as `<fi:segment>` under `<fi:busConfig>`
(see [bus configuration](../)).

### Identity + protocol

| Field | Type | Meaning |
|---|---|---|
| `segmentId` | UUID | Stable primary key — generated on creation, not editable. Survives rename, protocol switch, IP change. |
| `protocol` | Enum | `modbustcp` / `modbusrtu` / `ethercat` / `profibus` / `ethernetip`. Determines which bridge daemon starts. |
| `name` | String | User label (e.g. `"Halle1"`). Free choice, visible in tree + logs, **is** part of the IEC namespace (`anvil.Halle1.<Device>.<Var>`). |
| `enabled` | Bool | On/off switch. `false` = bridge is not started, devices stay offline. Default: `true`. |

### Interface + routing

| Field | Type | Meaning |
|---|---|---|
| `interface` | String | Network interface (`eth0`, `/dev/ttyUSB0`). Bridge passes it to the socket / serial API. |
| `bindAddress` | String (IP/CIDR) | Source IP for outbound TCP connections, e.g. `192.168.24.100/24`. Empty = OS picks automatically. |
| `gateway` | String (IP) | Default gateway for packets leaving the local subnet. Empty = no gateway. |
| `pollIntervalMs` | Int (ms) | Polling interval of the bridge. `0` = as fast as possible. Typical: `100` for Modbus TCP, `0` for EtherCAT. |

### Network settings (advanced)

For cases where OS defaults are not enough — typically: many
parallel TCP connections per slave, long-running sessions across
NAT, multiple subnets on one NIC.

| Field | Type | Meaning |
|---|---|---|
| `subnetCidr` | String (CIDR) | Local subnet of the segment. Allows per-device gateway overrides when the NIC carries multiple networks. |
| `sourcePortRange` | String `"min-max"` | TCP source-port pool, e.g. `30000-39999`. Empty = ephemeral OS range. Important when many parallel connections go to the same slave. |
| `keepAliveIdleSec` | Int (s) | Idle seconds before the first TCP keep-alive. `0` = OS default. |
| `keepAliveIntervalSec` | Int (s) | Distance between probes. `0` = OS default. |
| `keepAliveCount` | Int | Number of failed probes before a connection is declared dead. `0` = OS default. |
| `maxConnections` | Int | Connection-pool cap. `0` = unlimited. Protection against slaves with a hard connection limit. |
| `vlanId` | Int (1..4094) | 802.1Q VLAN tag. `0` = untagged. |

### Protocol-specific settings

The `settings` map (key/value) carries values that only make sense
for a specific protocol:

| Protocol | Typical settings |
|---|---|
| `modbustcp` | `port`, `timeout_ms` |
| `modbusrtu` | `serial_port`, `baud_rate`, `parity`, `stop_bits` |
| `ethercat` | `dc_sync_shift_ns`, `cycle_time_us` |
| `profibus` | `master_address`, `baud_rate` |

Plus protocol-independent: `log_level`, `log_file`.

---

## Edit path in ForgeIEC Studio

Both paths in the bus tree panel are equivalent:

| Action | Effect |
|---|---|
| **Single click** on a segment node | `FPropertiesPanel` (right) shows all fields as inline editors. Changes are written into the project on `editingFinished` + the dirty flag is set. |
| **Double click** | Modal dialog `FSegmentDialog` with the same field set, grouped into *General* / *Protocol* / *Advanced Network* / *Logging*. OK applies, Cancel discards. |

---

## Bridge lifecycle

When you create a segment with `enabled=true` and save:

1. `anvild` notices the new segment on the next project push
2. anvild's subprocess manager spawns the matching bridge daemon
   (`tongs-<protocol>`) with the segment ID as an argument
3. Bridge opens the configured interface + connects to each
   device
4. Live status flows via **Anvil zero-copy IPC** between bridge
   and PLC runtime — no TCP loopback latency
5. If the bridge crashes, anvild restarts the daemon
   automatically; the PLC logic continues uninterrupted

Bridge status per segment is reachable via MCP
`bellows.protocol_status`, or directly as a colour indicator in
the bus panel (green/yellow/red/grey).

---

## Example: Modbus TCP segment

```toml
[[bus_segments]]
segment_id     = "a3f7c2e1-7c4f-4e1a-9f9c-1a2b3c4d5e6f"
protocol       = "modbustcp"
name           = "Halle1"
enabled        = true
interface      = "eth0"
bind_address   = "192.168.24.100/24"
gateway        = ""
poll_interval  = 100

[bus_segments.settings]
port           = "502"
timeout_ms     = "2000"
log_level      = "info"
log_file       = "/var/log/forgeiec/halle1.log"
```

Effect:

- `tongs-modbustcp` starts on `eth0` with source IP
  `192.168.24.100`
- Polls all devices at 100 ms
- Allows up to 2000 ms per request before timeout
- Logs to `/var/log/forgeiec/halle1.log`
- IEC variables reachable as `anvil.Halle1.<Device>.<...>`

---

## See also

- [Bus configuration — schema overview](../) — 5-level namespace,
  FDD system, XML persistence
- [Bus devices](../devices/) — devices + modules + FDDs
- [Tongs bridge family](/news/tongs-bridges/) — fault model +
  bridge lifecycle
