---
title: "Sequential Function Chart Editor (SFC)"
summary: "Step-transition model for sequential control and mode machines"
---

## Overview

Sequential Function Chart (SFC) is the third graphic IEC 61131-3
language and describes **state-oriented sequences** through a
step-transition model — formally related to Petri nets. An SFC diagram
consists of a sequence of **steps** connected by **transitions** with
conditions. At any moment a subset of the steps is active; a step is
left when its outgoing transition becomes TRUE.

SFC is the natural language for **sequential control, mode machines,
and batch processes** — anything you would describe as "first this,
then that, except when ...".

## Editor layout

The SFC editor follows the same three-part scheme as FBD and LD:
toolbar at the top, QGraphicsView with grid + zoom + pan, variable
table on the right. The toolbar offers tools for every SFC element
type.

## Element types

### Step

A step is a **rectangular box** with a name. While it is active, the
actions associated with it run.

* **Initial step:** The entry point of the POU. Becomes active at
  program start. Drawn with a **double border** in the editor.
* **Follow-up steps:** Drawn with a single border. Become active when
  the preceding transition fires.

Ports: top (IN, from the previous transition), bottom (OUT, to the
next transition), right (connection to action blocks).

### Transition

A transition is a **short horizontal bar** on the vertical connection
line between two steps. To the right of the bar is the **condition**
— either an ST expression (e.g. `tmr.Q AND xReady`) or the output of
a function block.

When the condition becomes TRUE, the preceding step deactivates and
the following step becomes active.

### Action block

An action block describes **what happens while a step is active**. It
consists of two cells: the **qualifier** on the left and the **action
name** on the right (a reference to an ST action or an output
variable).

| Qualifier | Meaning |
|---|---|
| `N` | Non-stored — runs while the step is active (default). |
| `P` | Pulse — fires once for one cycle at step activation. |
| `S` | Set — set and remains active across step transitions. |
| `R` | Reset — clears an action previously set with `S`. |
| `L` | Limited — runs for at most the given time duration. |
| `D` | Delayed — starts only after the given delay. |

Several action blocks may be docked to one step.

### Divergence and convergence

A **divergence** branches the sequence into multiple paths, a
**convergence** joins them again. SFC has two kinds:

* **Selection (OR-divergence):** Exactly **one** of the paths is
  entered, depending on which transition condition becomes TRUE first.
  Drawn as a **single horizontal bar**.
* **Parallel (AND-divergence):** **All** paths become active
  simultaneously and run independently. Only when each one reaches the
  convergence point does the sequence move on. Drawn as a **double
  horizontal bar**.

### Jump

A jump item is a **downward arrow** carrying the name of the target
step. It transfers control from the current path to a named step —
typically used for "back to start" at the end of a sequence, or for
error handling ("jump to `Step_Error`").

## Application

SFC fits whenever a program has a clear **temporal sequence**:

* **Machine modes** — Init → Idle → Running → Cleanup → Idle.
* **Batch processes** — Fill → Heat → Mix → Drain.
* **Safety sequences** — performing stop sequences in a defined order
  ("first heater off, then pump off, then main contactor").
* **Process engineering** — reaction steps with delays and conditions.

Compared with an ST implementation of the same function, the SFC
version is significantly more readable — step order and branching
conditions are graphically obvious, whereas in ST a `CASE state OF`
construct conveys the same information only indirectly.

## Related topics

* [Function Block Diagram](../fbd/) — for the logic **inside** an
  action or a transition condition.
* [Ladder Diagram](../ld/) — alternative graphic language for simpler
  interlocking circuits.
* [Library](../library/) — timers (`TON`, `TP`) are common parts of
  transition conditions.
