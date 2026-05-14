---
title: "SFC elements"
summary: "Steps, transitions, actions, and the divergence/convergence patterns that compose a Sequential Function Chart."
weight: 10
iec_chapter: "6.7"
construct_kind: "graphical-element"
keywords: ["SFC", "step", "transition", "action", "divergence", "convergence"]
---

## Steps

A **step** represents a state the program can be in. The
diagram draws each step as a rectangle:

```
   +-----------+
   |  STEP_1   |
   +-----------+
```

A step is either **active** or **inactive** at any moment.
While active, all of the step's associated actions execute
every scan cycle. While inactive, none of its actions run.

The diagram has exactly one **initial step** — drawn as a
double-bordered rectangle:

```
   ##############
   #  INIT_STEP #
   ##############
```

Initial steps are active when the program starts; all other
steps start inactive.

## Transitions

A **transition** is the gate between two consecutive steps.
Drawn as a horizontal bar with a condition expression next to
it:

```
   +-----------+
   |  STEP_1   |
   +-----------+
        |
   ----------------     condition: xButton AND tonReady.Q
        |
   +-----------+
   |  STEP_2   |
   +-----------+
```

A transition fires when:
1. Its source step is currently active, AND
2. Its condition expression evaluates to `TRUE`.

When the transition fires, its source step deactivates and
its target step activates — atomically, in one cycle.

Transition conditions can be ST expressions, IL fragments,
LD micro-rungs, or FBD micro-diagrams — IEC accepts all four
languages for transitions, and the choice is per-transition.
The condition must evaluate to a single `BOOL`.

## Actions

An **action** is a piece of code attached to a step. Its body
can be in any of the four "real" languages (ST, IL, LD, FBD).
While the parent step is active, the action runs.

Actions have qualifiers that modify when they run:

| Qualifier | Meaning |
|---|---|
| `N` | "Non-stored" — runs every scan while the step is active |
| `S` | "Set" — latch ON until explicitly reset (R or R1) |
| `R` | "Reset" — latch OFF |
| `P` | "Pulse" — runs for one scan when the step activates |
| `P0` | "Pulse on deactivation" — runs for one scan when the step deactivates |
| `P1` | "Pulse on activation" — synonym of P |
| `D` | "Delay" — runs every scan after a configurable delay |
| `L` | "Limit" — runs for a configurable max duration |
| `SD` | "Stored Delay" |
| `DS` | "Delayed Stored" |
| `SL` | "Stored Limited" |

The default qualifier is `N` and is the right pick for almost
all uses.

## Divergence and convergence

When a single step can transition to one of several next
steps, use a **divergence**:

- **Alternative divergence** ("OR-divergence") — exactly one
  branch is taken, based on which transition fires first.
  Drawn with single horizontal lines forming the fork.
- **Parallel divergence** ("AND-divergence") — all branches
  activate simultaneously. Drawn with double horizontal lines.

The matching **convergence** rejoins them:

- **Alternative convergence** — any branch's terminal step
  joining a single horizontal line.
- **Parallel convergence** — all branches must be at their
  terminal steps simultaneously before the join transition
  evaluates. Drawn with double horizontal lines.

```
   STEP_1
     |
   --------       (alternative divergence)
   |   |
 STEP_A STEP_B
   |   |
   --------       (alternative convergence)
     |
   STEP_2

   STEP_1
     |
   ========       (parallel divergence)
   |   |
 STEP_A STEP_B   (run simultaneously)
   |   |
   ========       (parallel convergence — wait for both)
     |
   STEP_2
```

## Action blocks

A step may have multiple actions, drawn as stacked blocks
attached to the step:

```
   +-----------+    +---+----------------+
   |  STEP_1   |----+ N | OpenValve     |
   +-----------+    +---+----------------+
                    +---+----------------+
                    | P | LogStartEvent  |
                    +---+----------------+
```

The first column is the qualifier (`N`, `P`, `S`, …). The
second is the action name — either an action declared inside
the SFC POU, or a BOOL variable that gets driven (qualifier-
appropriate write semantics).

## ForgeIEC notes

ForgeIEC's SFC editor has the conventional toolbox of step,
transition, divergence, convergence and action elements.
Persistence is PLCopen XML.

The matiec backend compiles SFC by lowering it to ST with a
hand-rolled active-step bitmask plus a transition-evaluation
loop — the runtime overhead is minimal. Use SFC whenever the
sequential structure is the dominant feature of the logic;
fall back to a CASE-of-iStep state machine in ST when the
SFC formalism is overkill.

## IEC reference

IEC 61131-3 third edition (2013), clause **6.7** — "Graphical
languages" → "Sequential Function Chart (SFC)".

## matiec conformance

matiec implements steps, transitions and the action-qualifier
set per the standard. Divergence/convergence (both alternative
and parallel) are supported. The exact behaviour of the more
exotic qualifiers (`SD`, `DS`, `SL`) is implementation-defined
per the spec and matiec's behaviour matches the reference
implementation.
