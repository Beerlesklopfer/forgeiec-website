---
title: "Manufacturer data as first-class citizen: FDD system"
date: 2026-05-04
summary: "Device descriptions with embedded PDF data sheets, diagnostic-bit resolution, module picker — no more PDF hunting"
components: [studio]
---

{{< components "studio" >}}

## What it's about

Manufacturer data in automation is classically a **distribution
problem**: the data sheet lives as a PDF on a network drive, the
GSD/EDS/FDD file in another folder, and the diagnostic-bit table
in the appendix of the user manual — if not already lost.

ForgeIEC Studio treats **the manufacturer's FDD as the binding
source** and packs everything together: machine-readable device
description **plus** the PDF data sheet **plus** the
diagnostic-bit tables — all in **one file**, all accessible from
Studio.

---

## One file, everything inside

The FDD is held in the PLCopen FDD XML format. Data sheets land
as **CDATA-embedded PDFs** in the `<Document>` element. On import
Studio detects this, extracts the PDF, shows it in the documents
tab of the device properties panel — directly in the editor, no
external PDF reader needed.

Benefit: **one file = one complete device**. If you hand a machine
over as a tarball, the full manufacturer info is included.

---

## Diagnostic bits — structured, decodable

Vendor devices list their bits in the FDD's `<DiagnosticDecode>`
block:

```xml
<DiagnosticDecode bitOffset="3" length="1">
  <Description lang="DE">Drahtbruch Kanal 3</Description>
  <Description lang="EN">Wire break channel 3</Description>
  <Severity>warning</Severity>
</DiagnosticDecode>
```

Studio parses these blocks and shows them in the properties panel
under the **diagnostics tab** — with live value per bit from the
running PLC. You see immediately which bits are active and what
they mean, in German or English.

Via the MCP `catalog.diag_bits` it is also accessible to the AI
assistant — AI diagnostic loops can then answer concretely:

> "Module `Stachelbeere` reports wire break on channel 3 (severity
> warning, active since 14:32:05). Check the wiring to terminal X3."

---

## Module picker with protocol filter

For modular bus couplers (e.g. Weidmueller UR20 with ProfiNet IRT
coupler + a colourful module selection) every coupler has a
`<ModuleProtocol>` entry in its FDD that says which module
families it understands. Studio uses this for a **filtered
module picker**:

- You select the coupler
- Studio shows **only** the modules that are compatible with this
  coupler
- No 200-entry list to guess from by hand
- No accidental selection of an incompatible module

Background: commit `5fe1e69`. Spec reference: `bus-system-v1.md`
§7.

---

## FDD editor in Studio

In addition to the read path, there is also an **FDD editor** for
the case that a manufacturer FDD is incomplete or you have to
register your own component:

- **Diagnostics tab** — edit `<DiagnosticDecode>` in a structured
  way, bit offset + description + severity
- **Documents tab** — drop in a PDF, it becomes CDATA-embedded in
  the `<Document>` section
- **Geometry persist** — window positions + zoom levels are
  remembered per file

Source commit: `6774397` (diagnostics + documents tabs).

---

## Catalog performance — from 30 s to sub-second

Initially the **catalog auto-import** at Studio startup re-parsed
every FDD with its embedded PDF — cold start took **30+ seconds**
with a medium catalog.

Fix in commit `3ee7cd6`: no BLOB read in auto-import; the PDF is
loaded lazily on **click on the device**. Cold start: **sub-second**.

---

## Licence + distribution

ForgeIEC ships with a **built-in Weidmueller catalog** (commit
`66923df`):

- 100+ modules complete with data sheet + diagnostics
- Git-LFS-managed — `catalog/` directory in the source tree
- All licence notices embedded in the `<Vendor>` tags of the FDDs

Other manufacturers will follow. Custom FDDs can be imported via
`File → Import FDD` — when the manufacturer does not publish
PLCopen FDD itself, you can convert GSDML/EDS/ESI into the
ForgeIEC format via the FDD editor.

---

## What the commits delivered

- `66923df` — Weidmueller FDDs with CDATA-embedded PDFs + Git-LFS
- `5dc087c` — FDD-driven diagnostic-bit resolver + diagnostics tab
- `5fe1e69` — `<ModuleProtocol>`-based module-picker filter
- `6774397` — FDD editor with diagnostics + documents tabs
- `3ee7cd6` — cold-start performance: no BLOB read in auto-import
- `aea0d4f` — spec docs of the `<DiagnosticDecode>` section

Spec: `documentation/architecture/bus-system-v1.md` §7
(manufacturer data lifecycle).

---

## Where you use it

| You want … | How |
|---|---|
| Look at the data sheet of a module | Click in the bus tab, documents tab |
| Understand diagnostic bits of an active device | Diagnostics tab with live values |
| Maintain a missing FDD yourself | File → New FDD, editor tabs |
| AI diagnostics with plain-text answers | `catalog.diag_bits` MCP tool |
| Hand the machine over as a tarball | FDDs + data sheets are inside the project |

---

## Where to read more

- [Bus configuration](/help/bus-config/)
- Spec: `documentation/architecture/bus-system-v1.md` (source tree)
