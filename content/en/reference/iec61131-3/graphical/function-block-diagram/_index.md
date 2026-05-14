---
title: "Function Block Diagram (FBD)"
summary: "Boxes-and-wires notation. Function blocks are blocks, signals are wires."
weight: 20
---

## Function Block Diagram

FBD is the graphical "boxes and wires" language. Each function
block instance is drawn as a box with named input pins on the
left side and named output pins on the right; signals are wires
between pins. The visual closely matches the block diagrams
common in control engineering, which is why FBD is the language
of choice for control loops, filter chains and signal-conditioning
networks.

ForgeIEC exposes FBD via the same graph editor as LD; the
persisted form is PLCopen XML.

### Sub-pages

- [Elements](elements/) — blocks, wires, in/out variable
  elements, execution-order rules.
