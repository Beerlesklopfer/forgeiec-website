---
title: "Function Block Diagram Editor (FBD)"
summary: "Graphic wiring of functions, function blocks, and variables"
---

## Overview

Function Block Diagram (FBD) is one of the three graphic IEC 61131-3
languages supported by ForgeIEC Studio. An FBD program consists of
**function and function block calls** wired together — and to input and
output variables — via **explicit wire connections**. Unlike Ladder
Diagram, FBD has **no power rails**: every connection is a single wire
that carries one output pin to one or more input pins.

## Editor layout

The FBD editor is a three-part widget:

```
+---------------------------------------------+
| Toolbar (Select | Wire | Block | Var | ...) |
+--------------------------------+------------+
|                                |            |
|       QGraphicsView            |  Variable  |
|       Grid + Zoom + Pan        |  table     |
|                                |  (right)   |
|                                |            |
+--------------------------------+------------+
```

* **Toolbar at the top:** Tool switching (Select, Wire, Place Block,
  Place In-/Out-Variable, Comment, Zoom).
* **QGraphicsView:** The drawing surface with a background grid
  (10 px minor, 50 px major) and middle-mouse pan. Mouse wheel zooms
  around the cursor.
* **Variable table on the right:** Dockable, shows the local variables
  of the POU. Drag-and-drop from the table creates an
  in-/out-variable item in the editor.

## Tools

| Tool | Effect |
|---|---|
| **Select** | Pick, move, delete items. |
| **Wire** | Click an output port, then click an input port — the connection is created. |
| **Place Block** | Drop a function or function block from the library. The pin list (inputs left, outputs right) is taken from the library definition. |
| **InVar / OutVar** | Place an input or output variable item. The name is entered through a dialog and may be a GVL-, Anvil- or Bellows-qualified variable. |
| **Comment** | Free-text note without semantic effect. |

## Blocks and pins

A **block item** represents a call to a function (`ADD`, `SEL`, ...) or
a function block (`TON`, `CTU`, ...). The item shows the type name in
the header, below it the instance name (FB only), and on the sides the
ports:

```
        +---- TON -----+
        | tonA         |
   IN --| IN          Q|-- timeUp
   PT --| PT         ET|-- elapsed
        +--------------+
```

Inputs are **always on the left**, outputs **always on the right**.
Negated pins are marked with a small circle at the port.

## Library drag

From the library panel, any standard or user block can be **dragged and
dropped directly into the editor**. On release, the pin list is taken
from the library definition; for function blocks the editor
automatically creates a `VAR` instance entry in the local variable
section.

## Round-trip to ST

At compile time the ForgeIEC compiler translates the FBD body into
Structured Text. A topological sort of the blocks by data flow
determines execution order. Therefore: **any FBD body is semantically
equivalent to an ST body**, and the choice of language is purely a
matter of readability.

## Example — on-delay timer with `TON`

A `TON` (on-delay timer) delays an input signal by a configurable time.
In FBD you would

  * wire an **input variable** `start` into the `IN` pin of the `TON` instance,
  * wire an **input variable** with value `T#5s` into the `PT` pin,
  * connect the `Q` output to an **output variable** `lampe`.

In ST that looks as follows:

```text
PROGRAM PLC_PRG
VAR
    start  AT %IX0.0 : BOOL;
    lampe  AT %QX0.0 : BOOL;
    tmr    : TON;
END_VAR

tmr(IN := start, PT := T#5s);
lampe := tmr.Q;
END_PROGRAM
```

This is exactly the form the compiler generates from the FBD diagram —
the variable instance `tmr` is the `Block` box, and the two wires are
the two `:=` assignments.

## Related topics

* [Library](../library/) — which blocks the block picker offers.
* [Variables Panel](../variables/) — variable declaration and address pool.
* [Ladder Diagram](../ld/) — current-path-oriented sister language.
