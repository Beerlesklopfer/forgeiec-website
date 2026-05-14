---
title: "LD elements"
summary: "Contacts, coils, function blocks and the power-rail topology that defines a Ladder Diagram."
weight: 10
iec_chapter: "6.7"
construct_kind: "graphical-element"
keywords: ["LD", "contact", "coil", "rung", "power rail", "ladder"]
---

## The two power rails

Every LD program is drawn between two vertical lines:

```
| left rail                                 right rail |
|                                                      |
|---[ contact ]---[ contact ]---( coil )---------------|
|                                                      |
|---[ contact ]----+--( coil )-------------------------|
|                  |                                   |
|                  +--( coil )-------------------------|
```

The left rail is **always energised** (logical TRUE). A
horizontal "rung" connects the left rail to a coil on the
right; the coil energises if and only if there is a complete
TRUE path through the contacts.

A program may have many rungs; each is independent and runs
top-to-bottom in declaration order within one scan cycle.

## Contacts

| Symbol | Name | Conducts when |
|---|---|---|
| `--[ ]--` | Normally-Open contact | the named BOOL is TRUE |
| `--[/]--` | Normally-Closed contact | the named BOOL is FALSE |
| `--[P]--` | Positive-edge (rising) contact | the named BOOL just went FALSE→TRUE |
| `--[N]--` | Negative-edge (falling) contact | the named BOOL just went TRUE→FALSE |

The text label above each contact names the BOOL variable
that controls it. Contacts in **series** form a logical AND
(all must conduct); contacts in **parallel** (multiple lines
between two junctions) form a logical OR.

## Coils

| Symbol | Name | Action |
|---|---|---|
| `--( )--` | Standard coil | named BOOL := rung-state |
| `--(/)--` | Negated coil | named BOOL := NOT rung-state |
| `--(S)--` | Set coil | latches BOOL to TRUE while rung is TRUE; FALSE doesn't reset |
| `--(R)--` | Reset coil | latches BOOL to FALSE while rung is TRUE |
| `--(P)--` | Positive-pulse coil | BOOL := TRUE for one scan when rung rises |
| `--(N)--` | Negative-pulse coil | BOOL := TRUE for one scan when rung falls |

Multiple coils on parallel branches all see the same rung-state.

## Function blocks inline

A standard FB (TON, CTU, R_TRIG, …) appears as a box within
the rung. Inputs go in on the left, outputs on the right.
The rung-state can drive a BOOL input pin (typically the
enable input).

```
     +---------+
--+--| TON     |--+--( )---
  |  |IN     Q |  |
  +--|         |  |
     |PT    ET |
     +---------+
```

For non-trivial control logic, FBD or ST is usually clearer
than LD.

## ForgeIEC editor notes

The ForgeIEC graph editor exposes LD as a drag-and-drop
canvas; persisted form is PLCopen XML. The editor's
auto-layout keeps rungs aligned to the left rail and rejects
floating elements that aren't connected to the rail topology.

## IEC reference

IEC 61131-3 third edition (2013), clause **6.7** — "Graphical
languages" → "Ladder Diagram (LD)".

## matiec conformance

matiec compiles LD via the same backend as ST — the LD source
is converted to an internal IL representation and then
through the standard pipeline. All standard LD elements
above are supported.
