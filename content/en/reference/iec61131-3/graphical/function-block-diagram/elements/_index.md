---
title: "FBD elements"
summary: "Blocks, wires, in/out variables and the data-flow topology of Function Block Diagrams."
weight: 10
iec_chapter: "6.7"
construct_kind: "graphical-element"
keywords: ["FBD", "block", "wire", "input", "output", "function block diagram"]
---

## Blocks and wires

FBD's basic unit is the **block** — a rectangular shape with
named input pins on the left and named output pins on the
right. The block name appears at the top; the pins are
labelled with their formal-parameter names from the underlying
FUNCTION_BLOCK or FUNCTION declaration.

Blocks are connected by **wires** — straight or orthogonal
lines that run from an output pin to one or more input pins
elsewhere in the diagram. The wire carries the value
output by its source pin to every input pin it terminates on.

```
   +------+              +------+
   | TON  |              | CTU  |
xA-+IN  Q +--xB-->-->-+--+CU  Q +--xResult
   |      |             |       |
T#1s+PT ET|             |  R    |
   +------+             | iPV   |
                        +-------+
```

## Input and output variable elements

A **variable input** is a small box on the left edge of the
diagram that names a variable. The wire from this box
delivers the variable's current value to whatever input pin
it connects to.

A **variable output** is the mirror — a small box on the
right edge that names a destination variable. The wire that
terminates at this box assigns the wire's value to the
variable.

```
[xButton] >---->[CU pin of CTU]
[CTU.Q output] >---->[xLamp]
```

In ForgeIEC the editor labels these boxes with the full
three-level form (`Anvil.Pfirsich.T_1`, `Bellows.<Group>.<Var>`,
`GVL.<NS>.<Var>`) when the variable is a pool entry; bare
names for POU-locals.

## Execution order

The IEC standard says blocks in an FBD execute in
**data-flow order** — a block runs only after all the blocks
that feed its inputs have run. The standard does not pin down
exact ordering; matiec uses topological sort with stable tie-
breaking on the block's `localId` attribute (the editor
assigns these as you place blocks; renumbering is
implementation-defined).

Cycles in the data-flow graph need an FB instance with
internal storage to break them — e.g. an `R_TRIG` whose
output feeds back to a block whose output feeds back to the
R_TRIG's input. Without an FB break, matiec rejects the FBD
as having an unevaluable cycle.

## Connection points and execution-order pins

The PLCopen XML serialisation distinguishes:

- `connectionPointIn` / `connectionPointOut` — the source-
  and-target ends of a wire.
- `executionOrderId` — an integer hint to influence the
  topological ordering when ties exist.

ForgeIEC's editor exposes execution-order via a context-menu
"reorder" action; the persisted XML's `executionOrderId`
attribute is what matiec consumes.

## Mixing FBD with ST

A `PROGRAM` or `FUNCTION_BLOCK` body can be only one
language — you can't mix ST and FBD inside a single POU.
However:

- A FUNCTION_BLOCK type can be implemented in ST and
  **instantiated** as a block in an FBD. The FBD diagram
  treats the FB as a black box.
- An SFC step's action body can be FBD even if the rest of
  the project is ST.

## ForgeIEC editor notes

The ForgeIEC graph editor handles both LD and FBD on the
same canvas (the persisted XML distinguishes them per POU).
Auto-layout snaps blocks to a grid and routes orthogonal
wires automatically.

## IEC reference

IEC 61131-3 third edition (2013), clause **6.7** —
"Graphical languages" → "Function Block Diagram (FBD)".

## matiec conformance

matiec compiles FBD via internal conversion to IL/ST. All
standard graphical elements are supported. The execution-
order tie-breaking is matiec-specific (topological sort with
`localId` ordering); rely on `executionOrderId` rather than
visual position when the order matters.
