---
title: "Tongs — modular fieldbus bridges with a fault model"
date: 2026-05-05
summary: "One daemon per protocol, uniform status wire format, diagnostic bits from the FDD — no vendor plugin sprawl"
components: [studio, tongs, anvild]
---

{{< components "studio,tongs,anvild" >}}

## What it's about

A PLC platform is only as good as its fieldbus connection. But
every bus is different: Modbus TCP has no real diagnostics,
EtherCAT has a fully clocked slave state machine, Profibus has its
own fault classes, EtherNet/IP has CIP connections.

**Tongs** solves this with a **plug-in family**: one daemon per
protocol, controlled by anvild, with a **uniform fault layer** and
**structured diagnostic bits** from the device FDDs. Instead of a
mega driver with all protocols inside, a **modular component
family**.

---

## One daemon per protocol

| Daemon | Protocol | Status |
|---|---|---|
| `tongs-modbustcp` | Modbus TCP master + slave mode | productive |
| `tongs-ethercat` | EtherCAT master with DC sync | in progress |
| `tongs-profibus` | Profibus DP/PA | planned |
| `tongs-ethernetip` | EtherNet/IP CIP | planned |

All run under the **same** anvild subprocess manager. Lifecycle,
logging, auto-restart — shared, not re-invented per protocol.

---

## Uniform fault model

Spec `tongs-platform-v1.md` §5 defines a **shared fault grading**
across all bridges:

| Level | Meaning |
|---|---|
| `OK` | Device communicates, no faults |
| `WARN` | Functional, but diagnostic bits indicate pre-fault |
| `FAULT` | Device communicates but a safety function is triggered |
| `OFFLINE` | Device doesn't respond |
| `UNKNOWN` | Bus status not determinable (e.g. scanner off) |

Reported **uniformly** in Studio + anvild — regardless of whether
underneath is Modbus, EtherCAT or Profibus. Operator doesn't have
to learn a separate error table per bus.

Call via MCP: `bellows.protocol_status` returns the current fault
state per segment including diagnostic bits.

---

## Diagnostic bits — structured, not free text

For vendor devices (e.g. Weidmueller bus terminals) there are
**concrete diagnostic bits** in the status bytes:

- Bit 0: module missing
- Bit 1: short circuit at output
- Bit 2: wire break
- Bit 3: supply voltage out of spec
- …

These bits live in the manufacturer's **FDD** (Field Device
Description). ForgeIEC Studio:

1. Imports FDDs (including embedded PDF data sheets)
2. Parses the `<DiagnosticDecode>` sections
3. Shows per-bit meaning + severity in Studio's diagnostics tab
4. Makes resolved bits accessible via the `catalog.diag_bits` MCP tool

AI diagnostic loop: "Why doesn't `Motor_Ready` switch?" → AI calls
`bellows.protocol_status` + `catalog.diag_bits` and can answer in
**plain text**: "Module `Stachelbeere` reports wire break at
output 3."

---

## Per-segment own daemon process

Architectural benefit: **a crashing bridge does not take down the
whole master**. If the EtherCAT bridge hits a fresh slave bug and
dies, Modbus + Profibus + the PLC logic continue undisturbed.
anvild restarts the crashed bridge daemon automatically.

This differs from monolithic runtimes where a driver fault
brings the whole machine down.

---

## Bus configuration in `.forge`

In the `.forge` project format, bus segments are stored
structured:

```toml
[[bus_segments]]
name = "Modbus_HMI"
protocol = "modbustcp"
settings.host = "192.168.1.50"
settings.port = 502

[[bus_segments.devices]]
name = "Stachelbeere"
fdd_path = "catalog/weidmueller/UR20-FBC-PN-IRT-V2.fdd"
```

Studio renders this as a bus tree, generates codegen + auto-rolls
the matching tongs bridge daemon at save.

IEC access in ST code with a clear 5-level namespace:
`anvil.<segment>.<device>.Status.<var>` — e.g.
`anvil.Modbus_HMI.Stachelbeere.Status.WireBreak`.

---

## Plus: Anvil ABI probe — no more version roulette

Tongs bridges talk to anvild via **Anvil shared memory**. With
mixed versions between anvild + bridge, **silently inconsistent
data** used to be possible — bridge writes ABI variant A, anvild
reads variant B, nobody notices.

With the **ABI probe** (commits `7653cc5` + `9b17adc`) the type
hash of SHM topics is verified at connect. A mismatch immediately
throws a **Studio warning** with concrete version comparison —
instead of silent data corruption.

---

## What the commits delivered

- `83fe7d4` — `anvil.*` tool family (4 tools)
- `3c61445` — `bellows.protocol_status` + `tasks.cycle_overview`
- `9cc6dcd` — force-gate layers 1-3 (also affects bus I/O)
- `5dc087c` — FDD-driven diagnostic-bit resolver
- `5fe1e69` — module-picker filter via `<ModuleProtocol>` in the
  coupler FDD
- `66923df` — Weidmueller FDDs self-contained with CDATA PDFs +
  Git-LFS
- `6774397` — FDD editor: diagnostics tab + documents tab
- `7653cc5`, `9b17adc` — Anvil ABI probe layers 3a/3b
- `21759e7` — MCP-4a remote bind enables bus diagnostics over
  distance

Spec: `documentation/architecture/tongs-platform-v1.md`
+ `bus-system-v1.md` + `anvil-platform-v2.md` §13.

---

## Where you use it

| Setup | What you configure |
|---|---|
| Modbus TCP on a PLC | `tongs-modbustcp` + device in the bus tab |
| Multiple protocols mixed | one `tongs-*` per protocol, anvild orchestrates |
| Diagnostics in production | `bellows.protocol_status` via MCP or the Studio bus panel |
| Swap a device (Stachelbeere → Birne) | swap FDD, regenerate, deploy |

---

## Where to read more

- [Bus configuration](/help/bus-config/)
- [MCP tool families: anvil + bellows + bus system](/help/ai/tools/)
- Spec: `documentation/architecture/tongs-platform-v1.md`
  (source tree)
