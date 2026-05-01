---
title: "Add a variable"
summary: "The FAddVariableDialog — every field in one modal, range patterns for bulk creation, array wrapper"
---

## Overview

The **FAddVariableDialog** is the modal window used to add a new
variable to a POU or the pool. It collects every field in a single
step and shows a **live preview** of the resulting IEC ST declaration
right below the form — what you type immediately renders as a finished
`VAR ... END_VAR` snippet.

The dialog runs in two modes:

  - **Add mode**: empty fields, OK creates a new variable. Reached via
    the plus icon in the Variables panel or Ctrl+N in the POU editor.
  - **Edit mode**: double-click an existing variable in the panel — same
    dialog, every field pre-filled.

## Fields

| Field | Required | Meaning |
|---|---|---|
| **Name** | yes | Programmer-visible name. Validated against IEC identifier rules (letter + letters/digits/`_`). Used for bulk creation with a range pattern (see below). |
| **Type** | yes | Combo with IEC elementary types, standard FBs, project FBs, user data types. Array creation is handled by the wrapper checkbox. |
| **Direction** | depends on POU | Var-class — see below. |
| **Initial** | no | Initial value (`FALSE`, `0`, `T#100ms`, `'OFF'`). |
| **Address** | no | Only for VarList POUs. Empty = `pool->nextFreeAddress` auto-allocates on creation. |
| **Retain** | no | Checkbox — RETAIN, value survives a power cycle. |
| **Constant** | no | Checkbox — `VAR CONSTANT`, not writable at runtime. |
| **Array wrapper** | no | Wraps the selected type in `ARRAY [..] OF`. |
| **Documentation** | no | Free-text comment, stored as `<documentation>` in PLCopen XML. |

## Range pattern for bulk creation

Instead of typing `LED_0`, `LED_1`, ... `LED_7` individually you can
specify a **range pattern** in the name field:

| Input | Effect |
|---|---|
| `LED_0..7` | Creates eight variables `LED_0` through `LED_7`. |
| `LED_0-7` | Synonym, same effect. |
| `Sensor_1..3` | Creates three variables `Sensor_1` through `Sensor_3`. |

On every bulk creation the address is incremented if it is set:
`%QX0.0` → `%QX0.0`, `%QX0.1`, ..., `%QX0.7`.

## Array wrapper checkbox

If you want **one** variable declared as an array, tick the array
checkbox. Two spin boxes appear for the index range and the type is
wrapped at runtime as `ARRAY [..] OF <type>`.

| Type combo | Array checkbox | Index range | Resulting declaration |
|---|---|---|---|
| `INT` | off | — | `: INT;` |
| `INT` | on | `0..7` | `: ARRAY [0..7] OF INT;` |
| `BOOL` | on | `1..16` | `: ARRAY [1..16] OF BOOL;` |
| `T_Motor` (user struct) | on | `0..3` | `: ARRAY [0..3] OF T_Motor;` |

The wrapper deliberately lives on a checkbox rather than in the type
combo — that keeps the combo uncluttered and lets you build arrays of
anything without searching the combo.

## Type combo

The combo aggregates four sources into a single list:

  1. **IEC elementary types**: `BOOL`, `BYTE`, `WORD`, `DWORD`, `LWORD`,
     `INT`, `DINT`, `LINT`, `UINT`, `UDINT`, `ULINT`, `REAL`, `LREAL`,
     `TIME`, `DATE`, `TIME_OF_DAY`, `DATE_AND_TIME`, `STRING`, `WSTRING`.
  2. **Standard FBs** from the library: `TON`, `TOF`, `TP`, `R_TRIG`,
     `F_TRIG`, `CTU`, `CTD`, `CTUD`, `SR`, `RS`, ...
  3. **Project function blocks** — every FB declared in the current
     project (user library).
  4. **User data types** from `<dataTypes>`: STRUCTs, enums, aliases.

ARRAY templates do **not** appear in the combo — they go through the
wrapper checkbox.

## Direction (var-class) per POU type

Which direction values are offered depends on the POU type:

| POU type | Available direction |
|---|---|
| `PROGRAM` / `FUNCTION_BLOCK` / `FUNCTION` | `VAR` / `VAR_INPUT` / `VAR_OUTPUT` / `VAR_IN_OUT` / `VAR_TEMP` |
| `GlobalVarList` (GVL) | Fixed `VAR_GLOBAL` — combo hidden. |
| `AnvilVarList` | Fixed `VAR_GLOBAL` (auto-generated) — combo hidden. |
| Pool globals (no POU container) | No direction — the `%I`/`%Q` address sets it implicitly. |

## Edit mode

Double-clicking an existing variable in the Variables panel opens the
same dialog. Every field is pre-filled; on OK changes are routed
through `pou->renameVariable` / `pool->rebind` (so the `byAddress`
indices stay in sync). The dialog detects edit mode by `existing !=
nullptr`.

## Example — 8 LEDs in one block

Eight output LEDs as pool variables, in a single step:

  - **Name**: `LED_0..7`
  - **Type**: `BOOL`
  - **Direction**: hidden (pool global)
  - **Address**: `%QX0.0` (auto-increment)
  - **Initial**: `FALSE`

OK creates eight pool entries:

```text
LED_0  AT %QX0.0 : BOOL := FALSE;
LED_1  AT %QX0.1 : BOOL := FALSE;
LED_2  AT %QX0.2 : BOOL := FALSE;
LED_3  AT %QX0.3 : BOOL := FALSE;
LED_4  AT %QX0.4 : BOOL := FALSE;
LED_5  AT %QX0.5 : BOOL := FALSE;
LED_6  AT %QX0.6 : BOOL := FALSE;
LED_7  AT %QX0.7 : BOOL := FALSE;
```

The eight variables can then be selected in the Variables panel and
assigned to an HMI group via a bulk operation — e.g. `Set HMI
Group... -> Frontpanel`.

## Related topics

  - [Variable management](../) — the Variables panel with columns,
    filters and bulk operations.
  - [Project file format](../../file-format/) — how the pool is
    persisted as an `<addData>` block in PLCopen XML.
