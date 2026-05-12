---
title: "Bus configuration"
summary: "How ForgeIEC Studio manages fieldbus networks + devices + variable bindings — from manufacturer FDD to IEC-ST access"
---

{{< components "studio,tongs,anvild" >}}

## What it's about

The bus configuration in ForgeIEC Studio describes the **physical
topology of a plant**: which fieldbus networks run on which
interface, which devices hang on each, which variables are linked
to which device registers. It becomes part of the `.forge` project
file and drives the codegen pipeline + bridge daemon lifecycle.

```
.forge project
  Segments (fieldbus networks)
    Devices
      Modules (for modular couplers)
        Variables (bound through the address pool)
```

Per segment, `anvild` starts **exactly one bridge daemon**
(`tongs-modbustcp`, `tongs-ethercat`, ...). A crash in the EtherCAT
bridge does **not** take down your Modbus bridge — every bridge
daemon is managed individually + auto-restarted when needed.

---

## IEC-ST access: 5-level namespace

Variables from the bus system are reached in ST code through a
clear 5-level namespace:

```
anvil.<Segment>.<Device>.<Struct>.<Variable>
```

Example:

```text
IF anvil.Halle1.Stachelbeere.Status.WireBreak THEN
    Motor_Ready := FALSE;
END_IF;

anvil.Halle1.Maibeere.IO.DO_1 := Switch_State;
```

This is **not** a flat variable pool like many classic IDEs, but
a **real hierarchy** that codegen derives from the bus topology.
Tree-sitter-typed — autocomplete in the ST editor shows you the
struct members a device has.

Status variables (`Status.<Var>`) are **auto-generated TYPE
members**, not pool entries. They come from the
`<DiagnosticDecode>` section of the manufacturer's FDD (see next
section).

---

## Manufacturer data as first-class

Instead of maintaining PDF data sheets and FDD files separately,
ForgeIEC packs everything into **one** FDD file per device:

| Element | Content |
|---|---|
| `<Vendor>` | Manufacturer data + license |
| `<Identification>` | Part number, product name |
| `<ModuleProtocol>` | Which modules this coupler supports |
| `<DiagnosticDecode>` | Status-bit definitions (DE + EN) |
| `<Document>` | CDATA-embedded PDF data sheet |

Consequences:

- **Module picker** shows only modules that match the coupler —
  no guessing in a 200-entry list
- **Diagnostic bits** appear in the properties panel with live
  values + meaning
- **Data sheet** in the documents tab — no external PDF viewer
- **One file = one complete device** — handing a machine over as
  a tarball automatically includes the manufacturer info

Create your own FDDs via `File → New FDD` (diagnostics tab +
documents tab in the FDD editor).

More on the FDD system: [news post](/news/catalog-fdd/).

---

## Bridge fault model — uniform

All bridges (Modbus, EtherCAT, Profibus, EtherNet/IP) report their
status on the **same** 5-stage scale:

| Level | Meaning |
|---|---|
| `OK` | Device communicates, no faults |
| `WARN` | Functional, but diagnostic bits indicate a pre-fault |
| `FAULT` | Device communicates, a safety function has triggered |
| `OFFLINE` | Device doesn't respond |
| `UNKNOWN` | Bus status not determinable (e.g. scanner off) |

Accessible in Studio (bus panel status column) or via MCP:

```
bellows.protocol_status — snapshot of all segments + devices
catalog.diag_bits       — resolved diagnostic bits per device
project.bus_topology    — full topology as JSON
```

Operator + AI assistant see immediately which device is
misbehaving — regardless of the protocol underneath.

---

## Variable binding

I/O variables are **not** listed in the device entry. Instead,
every variable in the address pool carries a `busBinding`
attribute pointing to the device ID:

```
FVariable
  name:    "DI_1"
  address: "%IX0.0"     ← physical, allocated by the pool
  scope:   anvil.Stachelbeere
  flags:
    bellows_export: false    ← expose to HMI / OPC-UA?
    force_enabled:  false    ← allowed to be forced? (4-layer gate)
    monitor_enabled: true
  busBinding:
    deviceId:       <UUID-of-Stachelbeere>
    modbusAddress:  0
    count:          1
```

When you **bind** a variable to a device, the address moves
automatically from `%MX` (memory) to `%IX`/`%QX` (physical). When
you **unbind**, it returns to the memory range.

### Per-variable safety flags

Three separate flags control what a variable may do — all default
OFF:

- **`bellows_export`** — variable is exposed via bellowsd as an
  OPC-UA node + Modbus TCP server coil (HMI integration)
- **`force_enabled`** — the `F` checkbox may be set in the GUI;
  without this flag, forcing is already disabled in the code
  generator (layer 1 of the
  [4-layer defence](/help/ai/security/))
- **`monitor_enabled`** — variable appears in the live monitor
  stream (otherwise only local in the PLC)

That is the granularity: **no** "all or nothing" — every variable
is gated individually.

---

## Setup workflow in ForgeIEC Studio

| Step | Action |
|---|---|
| **1. Create segment** | Bus panel → `+ Segment` → enter protocol + interface |
| **2. Add device** | Right-click the segment → `+ Device` → pick FDD from catalog |
| **3. Add modules (modular coupler)** | Right-click the device → `+ Module` (filtered by `<ModuleProtocol>`) |
| **4. Bind variables** | In the Variables tab `F` column / bus binding editor — or via MCP `project.write.set_variable_scope` |
| **5. Set flags** | `B` checkbox for Bellows export, `F` for force, `M` for monitor |
| **6. Save + deploy** | `Build → Compile and Upload` — anvild starts the bridges + spawns the PLC |

Edit either in the **properties panel** (single click, saved
immediately) or in the **modal dialog** (double click, OK/Cancel).

---

## Bus configuration in `.forge` XML

The bus configuration is persisted as an `<addData>` extension at
project level (PLCopen TC6 conformant):

```xml
<project>
  <types>...</types>
  <instances>...</instances>

  <addData>
    <data name="https://forgeiec.io/v2/bus-config"
          handleUnknown="discard">
      <fi:busConfig xmlns:fi="https://forgeiec.io/v2">

        <fi:segment id="a3f7c2e1-..."
                    protocol="modbustcp"
                    name="Halle1"
                    interface="eth0"
                    bindAddress="192.168.24.100/24"
                    pollIntervalMs="100">

          <fi:device deviceId="b7f8d3a2-..."
                     hostname="Stachelbeere"
                     ipAddress="192.168.24.25"
                     slaveId="1"
                     catalogRef="weidmueller/UR20-FBC-PN-IRT-V2"/>

        </fi:segment>

      </fi:busConfig>
    </data>
  </addData>
</project>
```

`handleUnknown="discard"` makes sure PLCopen-conformant tools that
don't know about ForgeIEC ignore the section **without error**.
Conversely ForgeIEC reads unknown `<addData>` blocks from other
vendors and preserves them on save.

Detail schema:
- [Bus segments](segments/) — fields per segment + protocol-
  specific settings
- [Bus devices](devices/) — devices + modules + per-device overrides
- [`.forge` file format](../file-format/) — XML root + vendor
  extensions

---

## Supported protocols

| Protocol | `protocol` value | Medium | Bridge | Status |
|---|---|---|---|---|
| Modbus TCP | `modbustcp` | Ethernet | `tongs-modbustcp` | productive |
| Modbus RTU | `modbusrtu` | RS-485 | `tongs-modbusrtu` | in progress |
| EtherCAT | `ethercat` | Ethernet (DC) | `tongs-ethercat` | in progress |
| Profibus DP | `profibus` | Fieldbus | `tongs-profibus` | planned |
| EtherNet/IP | `ethernetip` | Ethernet (CIP) | `tongs-ethernetip` | planned |

---

## See also

- [Bus segments](segments/) — fields + protocol settings
- [Bus devices](devices/) — device config + FDD integration
- [Catalog + FDD system](/news/catalog-fdd/) — manufacturer data
  as first-class
- [Tongs bridge family](/news/tongs-bridges/) — fault model +
  bridge lifecycle
- [Security model](/help/ai/security/) — 4-layer defence for
  force settings
- [`.forge` file format](../file-format/)
