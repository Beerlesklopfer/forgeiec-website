---
title: "Variable Management"
summary: "The Variables panel as the central view onto the FAddressPool — columns, filters, bulk operations, safety switches"
---

## Overview

The **Variables panel** is the central view onto the **FAddressPool** —
the single source of truth for every variable in a ForgeIEC project.
Each variable exists exactly once in the pool, keyed by its IEC address
(`%IX0.0`, `%QW3`, ...). Containers such as GVL, AnvilVarList, HmiVarList
or POU interfaces are only **views** onto this pool — no variable lives
in two stores in parallel.

```
FAddressPool  (single source of truth)
   |
   +-- FAddressPoolModel  (Qt table)
         |
         +-- FVariablesPanel  (filters + bulk ops + clipboard)
               |
               +-- Tree filter sets FilterMode + tag
```

The panel docks at the bottom of the main window and mirrors every
change immediately into every other view (POU editor, ST compiler,
PLCopen-XML save).

## Columns

The table has **15 columns**; each can be toggled individually via the
header context menu — every POU editor instance stores its column
visibility independently.

| Column | Content |
|---|---|
| **Name** | Programmer-visible name. Qualified pool entries appear with their full path: `Anvil.Pfirsich.T_1`, `Bellows.Stachelbeere.T_Off`, `GVL.Motor.K1_Mains`. |
| **Type** | IEC elementary type or user-defined type. Arrays show as `ARRAY [0..7] OF BOOL`. |
| **Direction** | IEC var-class: `VAR` / `VAR_INPUT` / `VAR_OUTPUT` / `VAR_IN_OUT` / `VAR_TEMP` for POU locals; `in`/`out` for pool globals (derived from `%I` vs. `%Q`). |
| **Address** | IEC address — the primary key. `%IX0.0` for a bit input, `%QW1` for a word output, `%MX10.3` for a marker bit. |
| **Initial** | Initial value (`FALSE`, `0`, `T#100ms`, `'OFF'`). Loaded into the variable on first cycle. |
| **Bus Device** | UUID of the bus device (Modbus slave etc.) this variable is bound to — editable as a combo box. |
| **Bus Addr** | Modbus register offset relative to the slave (`0`, `1`, ...). |
| **R** (Retain) | Checkbox — does the value survive a power cycle? |
| **C** (Constant) | Checkbox — IEC constant (`VAR CONSTANT`), value not writable at runtime. |
| **RO** (ReadOnly) | Checkbox — read-only from program code. |
| **Sync** | Multi-task sync class (`L`/`A`/`D`), produced by the last ST-compiler run. |
| **Used by** | Which tasks read/write this variable, e.g. `PROG_Fast (R/W), PROG_Slow (R)`. |
| **Monitor** / **HMI** / **Force** | Per-variable safety switches. **Cluster A** in the backlog — explicit opt-ins, distinct from the `hmiGroup` tag. The ST compiler verifies before codegen that Force/HMI access only targets variables that carry the flag. |
| **Live** | Runtime value in online mode (fed by the anvild live-value store; hidden when disconnected). |
| **Scope** | Oscilloscope-visibility checkbox — sends the variable to the scope panel. |
| **Documentation** | Free-text comment. |

## Filter modes

The panel does not show the entire pool at once — the **project tree on
the left** picks which slice is visible. Clicking a tree node makes the
main window set `FilterMode` plus tag:

| FilterMode | Shows |
|---|---|
| `FilterAll` | The whole pool — no tag restriction. |
| `FilterByGvl` | Variables with `gvlNamespace == tag` (e.g. only `GVL.Motor`). |
| `FilterByAnvil` | Variables with `anvilGroup == tag` (one Anvil IPC group). |
| `FilterByHmi` | Variables with `hmiGroup == tag` (one Bellows HMI group). |
| `FilterByBus` | Variables with `busBinding.deviceId == tag` (all variables of one bus device). |
| `FilterByModule` | Like `FilterByBus`, plus `moduleSlot` — tag format `hostname:slot`. |
| `FilterByPou` | POU locals — variables with `pouInterface == tag`. |
| `FilterCommentsOnly` | Only comment dividers, no variables. |

## Filter axes (composable)

Above the table sit four further axes that all act in parallel on top
of the tree filter:

  - **Free-text search** over name, address and tags — `to` finds `T_Off`.
  - **IEC type filter** as a combo (`all` / `BOOL` / `INT` / `REAL` / ...).
  - **Address-range filter**: `all` / `%I` (inputs) / `%Q` (outputs) /
    `%M` (markers); within `%M` further by word size (`%MX` / `%MW` /
    `%MD` / `%ML`).
  - **TaggedOnly toggle** — hides every pool entry without any container
    tag (useful to find an "orphaned" pool).

Every filter is AND-combined: anything that does not match all active
axes is hidden.

## Multi-select + bulk operations

As in any Qt table: Shift-click and Ctrl-click select ranges or
individual rows. The context menu on the selection offers:

  - **Set Anvil Group...** — sets `anvilGroup` on every selected variable.
  - **Set HMI Group...** — same for `hmiGroup`.
  - **Set GVL Namespace...** — same for `gvlNamespace`.
  - **Clear Tag** — strips the tag of the active filter mode.
  - **Toggle Monitor / HMI / Force** — bulk toggle of the safety switches.

Every bulk edit goes through `FAddressPoolModel::applyToRows`, results
in a single `dataChanged` signal, and is undoable as one undo step.

## Clipboard (copy / cut / paste)

Selected variables can be copied — **with all tags and flags** — and
pasted into another view. The payload uses two formats:

  - **Custom MIME** (`application/x-forgeiec-vars+json`) as the roundtrip
    vehicle carrying full pool information.
  - **TSV plain text** as a fallback for Excel / text editors.

On **paste** the panel automatically retargets the container tags onto
the **active filter mode**: copy from `FilterByAnvil` (group `Pfirsich`)
and paste into `FilterByHmi` (group `Stachelbeere`) and the variables
drop their `anvilGroup` and pick up `hmiGroup = Stachelbeere`.
Conflicting addresses and names are deduplicated (`T_1` → `T_1_1`).

## Drag/drop into HmiVarList

Variables can be dragged from the main panel into a HmiVarList POU.
The editor then automatically sets the variable's **HMI export flag**
and writes the HMI group as a tag — the Bellows export is now armed.

## Per-variable safety switches

Three per-variable switches, each requiring an explicit opt-in:

  - **HMI** — allows Bellows to read/write the variable.
  - **Monitor** — allows live observation in online mode.
  - **Force** — allows forcing a runtime value.

These flags are **separate from the `hmiGroup` tag**. The tag describes
group membership; the flag activates the effect. Before each codegen
the ST compiler verifies that every Bellows or Force access targets a
variable whose flag is set — otherwise it raises a compile error.

## Related topics

  - [Add a variable](add/) — the `FAddVariableDialog` with range
    patterns and the array wrapper.
  - [Project file format](../file-format/) — how the pool is persisted
    as an `<addData>` block in PLCopen XML.
  - [Library](../library/) — how function blocks see their instances in
    the pool.
