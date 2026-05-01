---
title: "Library (Function Blocks + Functions)"
summary: "IEC 61131-3 standard library + ForgeIEC extensions + user-defined blocks"
---

## Overview

The ForgeIEC library is the central collection of all reusable building
blocks an application program can call from a `.forge` project — covering
both IEC 61131-3 standardised function blocks and functions, and project-
specific or ForgeIEC-specific extensions.

The library is shown in the **Library panel** (default dock: right-hand
sidebar). Press **F1** while the Library panel has focus to open this
page.

```
Library
+-- Standard Function Blocks    (Bistable, Edge, Counter, Timer, ...)
+-- Standard Functions          (Arithmetic, Comparison, Bitwise, ...)
+-- User Library                (project-specific blocks)
```

The library currently ships **almost 100 blocks** and **just over 30
functions**. Each entry carries:

  - **Name** (e.g. `TON`, `JK_FF`)
  - **Pin list** (inputs + outputs with type + position)
  - **Type** (`FUNCTION_BLOCK` with state, or `FUNCTION` stateless)
  - **Description** + **help text** with usage notes
  - **Code example** (visible in the Library Help panel)

## Category tree

### Standard Function Blocks

| Group | Blocks |
|---|---|
| **Bistable** | `SR`, `RS` — set/reset with priority |
| **Edge Detection** | `R_TRIG`, `F_TRIG` — rising/falling edge |
| **Counters** | `CTU`, `CTD`, `CTUD` — count up / down / both |
| **Timers** | `TON`, `TOF`, `TP` — on-delay / off-delay / pulse |
| **Motion** | profiles, ramps, trajectories (in preparation) |
| **Signal Generation** | generator FBs for test and validation signals |
| **Function Manipulators** | hold, latch, history |
| **Closed-Loop Control** | PID, hysteresis, two-point |
| **Application** *(ForgeIEC)* | `JK_FF`, `DEBOUNCE` — application-near blocks that proved universally useful in practice |

### Standard Functions

| Group | Contents |
|---|---|
| **Arithmetic** | `ADD`, `SUB`, `MUL`, `DIV`, `MOD` (on any ANY_NUM type) |
| **Comparison** | `EQ`, `NE`, `LT`, `LE`, `GT`, `GE` |
| **Bitwise** | `AND`, `OR`, `XOR`, `NOT` (on ANY_BIT — see `help/st`) |
| **Bit Shift** | `SHL`, `SHR`, `ROL`, `ROR` |
| **Selection** | `SEL`, `MAX`, `MIN`, `LIMIT`, `MUX` |
| **Numeric** | `ABS`, `SQRT`, `LN`, `LOG`, `EXP`, `SIN`, `COS`, `TAN`, `ASIN`, `ACOS`, `ATAN` |
| **String** | `LEN`, `LEFT`, `RIGHT`, `MID`, `CONCAT`, `INSERT`, `DELETE`, `REPLACE`, `FIND` |
| **Type Conversion** | `BOOL_TO_INT`, `REAL_TO_DINT`, `STRING_TO_INT`, ... |

### User Library

Project-defined function blocks and functions — anything declared as
`FUNCTION_BLOCK` or `FUNCTION` automatically lands in this category and
is callable from anywhere in the project, just like the standard blocks.

## Library panel — usage

| Action | Effect |
|---|---|
| **Search** (lens at the top) | Filters the tree view by block name — typing `to` finds `TON`. |
| **Double-click** on a block | Opens the block help in a detail pane: pin descriptions + code example. |
| **Drag** onto the ST editor | Inserts the block call at the cursor position, including the instance declaration in the local `VAR_INST` section. |
| **Right-click > "Insert Call..."** | Same as drag, via context menu. |
| **F1** on a block | Opens this page. |

## Example 1 — Button debounce with `DEBOUNCE`

`DEBOUNCE` filters short noise pulses out of a mechanical button contact.
`Q` only changes once `IN` stays stable for the full `T_Debounce` duration —
on both rising and falling edges.

### Pin layout

| Pin | Direction | Type | Meaning |
|---|---|---|---|
| `IN`         | INPUT  | `BOOL` | Raw input (typically `%IX`, mechanically bouncing) |
| `tDebounce`  | INPUT  | `TIME` | Minimum stable time (typically `T#10ms`...`T#50ms`) |
| `Q`          | OUTPUT | `BOOL` | Debounced output |

### Code example

PROGRAM body that debounces a pushbutton on `%IX0.0` and forwards the
debounced signal as a single-shot edge to a self-holding contactor:

```text
PROGRAM PLC_PRG
VAR
    button_raw      AT %IX0.0 : BOOL;       (* bouncing contact *)
    button_clean    : BOOL;                  (* after DEBOUNCE *)
    button_pressed  : BOOL;                  (* single-shot per press *)
    relay_lamp      AT %QX0.0 : BOOL;        (* lamp as self-hold *)
    fbDeb           : DEBOUNCE;              (* instance *)
    fbTrig          : R_TRIG;                (* edge detector *)
END_VAR

fbDeb(IN := button_raw, tDebounce := T#20ms);
button_clean := fbDeb.Q;

fbTrig(CLK := button_clean);
button_pressed := fbTrig.Q;

(* Self-hold: toggle on every rising edge *)
IF button_pressed THEN
    relay_lamp := NOT relay_lamp;
END_IF;
END_PROGRAM
```

`DEBOUNCE` is internally built from two `TON` blocks (high and low
direction) — one drives `Q` to TRUE only after `T_Debounce` of active
`IN`, the other drives it to FALSE only after `T_Debounce` of inactive
`IN`. This makes the filter symmetric: neither contact bouncing on press
nor on release produces a glitch.

> **Typical use:** mechanical pushbuttons, limit switches, contact-based
> sensors. For a "single shot per press" — as above — chain an `R_TRIG`
> after `Q`.

## Example 2 — Self-hold with mode override (`JK_FF`)

`JK_FF` is a toggle flipflop with built-in button debounce. On every
stable rising edge of `xButton` it flips `Q` between TRUE and FALSE — so
that a plain pushbutton becomes an "on/off" switch **without** the
application program having to wire DEBOUNCE + R_TRIG + toggle logic
together by hand.

### Pin layout

| Pin | Direction | Type | Meaning |
|---|---|---|---|
| `xButton`    | INPUT  | `BOOL` | Raw button contact (bouncing) |
| `tDebounce`  | INPUT  | `TIME` | Debounce time (typically `T#20ms`) |
| `J`          | INPUT  | `BOOL` | "Set" (forces `Q` to TRUE while active) |
| `K`          | INPUT  | `BOOL` | "Reset" (forces `Q` to FALSE while active) |
| `Q`          | OUTPUT | `BOOL` | Current state |
| `Q_N`        | OUTPUT | `BOOL` | Negated state (`NOT Q`) |
| `xStable`    | OUTPUT | `BOOL` | TRUE while `xButton` has been stable for `tDebounce` |

### Code example

A lamp control with three buttons: `T1` toggles the lamp, `T_Mains` forces
it on (e.g. "main light on everywhere"), `T_Off` forces everything off:

```text
PROGRAM PLC_PRG
VAR
    bButtons     AT %IX0.0 : ARRAY [0..3] OF BOOL;
    relay_lamp   AT %QX0.0 : BOOL;
    fbToggle     : JK_FF;
END_VAR

fbToggle(
    xButton    := bButtons[0],   (* toggle button T1 *)
    tDebounce  := T#20ms,
    J          := bButtons[1],   (* main light ON while held *)
    K          := bButtons[2]    (* main light OFF while held *)
);

relay_lamp := fbToggle.Q;
END_PROGRAM
```

Truth table of the `J`/`K` inputs:

| `J` | `K` | Behaviour |
|---|---|---|
| FALSE | FALSE | Toggle on every debounced press |
| TRUE  | FALSE | Q := TRUE (set, overrides toggle) |
| FALSE | TRUE  | Q := FALSE (reset, overrides toggle) |
| TRUE  | TRUE  | undefined — avoid |

`xStable` lets you implement "button is currently held" logic (e.g. a LED
visualising the press without having to wait for the toggle effect to
land).

## Library sync between editor and PLC

The standard library lives in two places:

  - **Editor side:** `editor/resources/library/standard_library.json`
    (compiled into the `.exe` via the Qt resource system).
  - **PLC side:** anvild submodule, same JSON file, included by the
    `make` step on the uploaded C sources.

The **library sync** compares SHA-256 of both versions on connect. On
drift a hint appears in the Output panel; the reaction is configurable:

  - `Preferences > Library > Auto-Push` off (default): manual push via
    `Tools > Sync Library`. Protects a production runtime against
    accidental overwrite from an older editor.
  - `Preferences > Library > Auto-Push` on: drift triggers an automatic
    push. Useful in dev setups with a single programmer.

## ForgeIEC extensions

The following blocks are not standardised in IEC 61131-3 but ship as part
of the standard library because their use proved universally helpful in
practice:

| Block | Purpose |
|---|---|
| `JK_FF` | Toggle flipflop with built-in button debounce (see Example 2). |
| `DEBOUNCE` | Symmetric button debounce (see Example 1). |

These blocks live under *Standard Function Blocks / Application* and are
flagged `isStandard: true` in the JSON source, marking them as
"non-deletable" (i.e. they cannot be accidentally removed via the Library
panel).

## Adding your own blocks to the User Library

Every `FUNCTION_BLOCK` and `FUNCTION` declaration in the current project
automatically lands under **User Library**. Visibility timing:

  1. **In the Library panel:** immediately after declaring + saving the POU.
  2. **In the code completer (Ctrl-Space):** immediately.
  3. **In the FBD/LD editor as a block:** immediately.
  4. **On the PLC** after `Compile + Upload`.

To reuse a block across projects, export the POU via
`File > Export POU...` as a `.forge-pou` file and import it in the target
project — a project-spanning "workspace library" is on the backlog.

## Related topics

- [Structured Text syntax](../st/) — how a block call looks in ST.
- [Function Block Diagram editor](../fbd/) — how a block is wired
  graphically.
- [Variables Panel](../variables/) — how the address pool sees the
  instance.
