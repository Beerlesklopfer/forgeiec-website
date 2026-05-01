---
title: "Ladder Diagram Editor (LD)"
summary: "Circuit-diagram metaphor: power rails, contacts, coils"
---

## Overview

Ladder Diagram (LD) is the oldest of the three graphic IEC 61131-3
languages and follows the **circuit-diagram metaphor**: between a left
and a right **power rail**, horizontal **current paths** (rungs) carry
the signal. On every rung, contacts sit on the left (in series) and
coils on the right; depending on the variable state they either "pass"
or "block" the current. LD is well suited to simple control logic —
limit switches, latching circuits, interlocks — and is highly readable
to electrical planners.

## Editor layout

The LD editor has the same structure as the FBD editor (toolbar at the
top, QGraphicsView with grid + zoom + pan, variable table on the right),
with two specifics:

* **Left power rail** and **right power rail** are permanent items in
  the diagram. They cannot be moved and grow vertically with the number
  of rungs.
* The toolbar adds buttons for LD symbols (contacts, coils, edge
  triggers) and an `Add Rung` button which inserts a new rung connection
  between the power rails.

## Symbols

### Contacts (left side of the rung)

| Symbol | Meaning |
|---|---|
| `--\| \|--` | **NO contact** — passes when the variable is TRUE |
| `--\|/\|--` | **NC contact** — passes when the variable is FALSE |
| `--\|P\|--` | **Rising-edge contact** — passes for one cycle on a rising edge |
| `--\|N\|--` | **Falling-edge contact** — passes for one cycle on a falling edge |

Contacts in series act as logical **AND**, parallel paths as logical
**OR**.

### Coils (right side of the rung)

| Symbol | Meaning |
|---|---|
| `--( )` | **Standard coil** — writes the current path state into the variable |
| `--(/)` | **Negated coil** — writes the inverted state |
| `--(S)` | **Set coil** — sets the variable to TRUE and latches it (even if the path opens later) |
| `--(R)` | **Reset coil** — sets the variable to FALSE and latches it |

Set/reset pairs implement a latching circuit without explicit
IF-THEN logic.

### Function blocks on the rung

Functions and function blocks from the library can be inserted **inline
between contacts and coils**. The LD editor draws them as a horizontal
box with pin lists on the right and left — semantically identical to
the FBD block. Typical uses: timers (`TON`), counters (`CTU`),
comparators (`GT`, `EQ`).

## Example — latching circuit with stop priority

A classic relay circuit: a start button `xStart` turns on a motor
`qMotor`, a stop button `xStop` turns it off. As long as `xStart` was
pressed at least once and `xStop` is not pressed, the motor stays on
(self-holding).

```text
        |                                              |
        |   xStart      xStop                          |
   +----| |---+--|/|---+-----------------------( )----+
        |    |         |                       qMotor  |
        |    |         |                                |
        |   qMotor     |                                |
        +----| |-------+                                |
        |                                              |
```

Read as a sentence:

  * `xStart` (NO) **or** `qMotor` (self-holding contact, NO) — in parallel,
  * **and** `xStop` (NC) — in series,
  * drive the coil `qMotor`.

At compile time the LD compiler translates this rung to:

```text
qMotor := (xStart OR qMotor) AND NOT xStop;
```

This is the simplest form of a latch with stop priority. If both
buttons are pressed at the same time, `xStop` wins because the NC
contact opens the path.

## Related topics

* [Function Block Diagram](../fbd/) — data-flow-oriented sister language.
* [Library](../library/) — function blocks for inline use on the rung
  (`TON`, `CTU`, `JK_FF`, `DEBOUNCE`).
* [Variables Panel](../variables/) — address pool and variable binding.
