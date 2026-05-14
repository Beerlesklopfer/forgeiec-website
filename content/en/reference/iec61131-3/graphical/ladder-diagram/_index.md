---
title: "Ladder Diagram (LD)"
summary: "Relay-ladder notation: rungs of contacts and coils between two power rails."
weight: 10
---

## Ladder Diagram

LD borrows its visual form from electrical relay schematics
drawn between two vertical "power rails": each horizontal rung
runs from the left rail to the right rail and contains a
sequence of normally-open / normally-closed contacts on the
input side and one or more coils on the output side. A coil
energises when current can flow from the left rail through its
rung to the right rail.

Despite the visual heritage, LD has been a programming language
in IEC 61131-3 since the first edition. Function blocks can
appear inline as boxes between contacts and coils — the LD
program is a graph, not just a contact-coil diagram.

ForgeIEC exposes LD via the same graph editor as FBD; the
persisted form is PLCopen XML.

### Sub-pages

- [Elements](elements/) — contacts, coils, inline FBs, the
  power-rail topology.
