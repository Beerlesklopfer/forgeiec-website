---
title: "IO-list roundtrip: a CSV bridge between electrician and programmer"
date: 2026-05-14
summary: "bus.import_iolist + bus.export_iolist — 14-column CSV with EPLAN-property headers, idempotent import, no variable invention"
components: [studio]
---

{{< components "studio" >}}

## What it's about

In machine engineering, two worlds work in parallel on the same
plant: the **electrician** draws the wiring diagram in EPLAN and
assigns a PLC address to every terminal point — the **programmer**
writes the IEC logic against exactly those addresses. Until now,
this bridge was maintained over email: a PDF excerpt, a
spreadsheet copy-paste, a manual update. Every encoder swap,
every re-wiring cost a synchronisation round.

With the **MCP-Bus-3 sprint**, ForgeIEC Studio and EPLAN P8 can
exchange their IO lists directly — through a 14-column CSV with
EPLAN-property headers, **bidirectional and idempotent**.

## The convention

A ForgeIEC IO list is a **UTF-8/BOM/`;`-separated** CSV with
headers derived directly from EPLAN's PLC properties (TechTipp
"Übersicht der SPS-Eigenschaften", AML AR APC):

| Column | EPLAN prop | ForgeIEC mapping |
|---|---|---|
| `Konfigurationsprojekt` | 20161 | project name |
| `SPS-Station: Name` | 20408 | CPU name |
| `Bus-System` | 20308 | segment protocol (modbustcp/...) |
| `Physikalisches Netz: Name` | 20413 | **segment identity** |
| `Bus-Adresse` | 20311 | device IP |
| `Hostname` | 20309 | **device identity** (= Anvil namespace) |
| `BMK` | 20006 | equipment designation |
| `Funktionstext` | 20031 | variable doc |
| `Symbolische Adresse` | 20404 | **variable identity** |
| `Adresse` | 20400 | IEC address (`%IX0.0`, ...) |
| `Datentyp` | 20405 | BOOL/INT/REAL/... |
| `Symbolische Adresse: Gruppe` | 20610 | AnvilVarList name |
| `Bus-Richtung` | (ForgeIEC) | in/out |
| `Modbus-Adresse` | (ForgeIEC) | numeric Modbus address |

## Why not "EPLAN CSV"?

Web research (EPLAN help portal, TechTipp Plattform 2027) makes
it clear: **EPLAN P8 has NO universal IO-list CSV format**. The
primary data exchange runs over **AutomationML AR APC** (XML);
CSV schemas vary per PLC vendor (different vendor toolchains,
each with its own export plug-in) and per release version.
What does exist are EPLAN's **PLC properties** with unique
property IDs — we use those as column names but explicitly do
NOT brand this as an "EPLAN CSV". It's a **ForgeIEC IO-list
format** that's compatible with EPLAN exports carrying the same
columns.

## Idempotency and safety discipline

The importer deliberately does **three things NOT**:

1. **No variable invention.** Variables are materialised by the
   FDD path (`bus.add_module` / `bus.replace_device`). If the
   CSV mentions a variable that doesn't exist in the pool, the
   row is counted as `variables_skipped` — never created as a
   new pool variable. New variables go through the FDD.
2. **No FDD materialisation for new devices.** If the CSV
   contains a hostname the project doesn't know, the device is
   created **empty** — the operator must follow up with
   `bus.replace_device` against the right coupler FDD to pull
   in the module structure.
3. **No atomic transactions.** Rows that fail to parse end up in
   `errors[]`, the rest commits. Partial imports are intentional
   — EPLAN exports often carry rows with empty addresses
   (documentation entries) that the operator wants to import
   anyway.

The **roundtrip guarantee** is hard: a `bus.export_iolist`
immediately followed by `bus.import_iolist` on an unchanged
project MUST yield
`{ segments_created: 0, devices_created: 0, variables_updated: 0,
errors: [] }`. Verified end-to-end against the Ackersteuerung
test plant (2 segments, 6 devices, 100+ pool variables).

## Daily workflow

```
Electrician (EPLAN P8)             Programmer (ForgeIEC)
======================             =====================
1. Draws wiring diagram
2. Assigns PLC addresses
3. Exports assignment list
   → ackersteuerung.csv
                          ─ mail ─►
                                   4. File → Import → IO list...
                                   5. (Confirm dialog: cascade impact)
                                   6. Pool variables get new
                                      addresses + function texts
                                   7. ST code keeps working against
                                      the old symbolic names —
                                      no re-compile required
```

Both tools (`bus.import_iolist` / `bus.export_iolist`) are
available as **MCP tools** (LLM-driven) AND through the **File →
Import / Export** menu (operator-driven) — bit-identical
behaviour. The IO-list actions also live under **Tools → Import /
Export**, because they conceptually belong to the bus family,
not to POU code.

## Next steps

- **Phase 4 (backlog):** BMK roundtrip persistence — currently
  the BMK column is passed through informationally. A future
  schema attaches it as a variable annotation.
- **AutomationML AR APC:** the "real" EPLAN standard. Once a
  user requests it, we'll add `bus.import_aml` / `bus.export_aml`
  alongside the CSV variant.
