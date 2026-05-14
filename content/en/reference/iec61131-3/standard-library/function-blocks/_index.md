---
title: "Standard function blocks"
summary: "Built-in FBs from IEC 61131-3 — bistables, edge detectors, counters, timers."
weight: 20
---

## Standard function blocks

The Function Blocks defined in IEC 61131-3 second annex
(normative) — every implementation, including matiec, must
provide them. They split into four families:

### Bistables

State elements with `S` / `R` set / reset inputs. Behaviour
depends on which input has priority.

- **[`SR`](sr/)** — Set-dominant bistable. `S1` (set) wins
  over `R`.
- **[`RS`](rs/)** — Reset-dominant bistable. `R1` (reset) wins
  over `S`.

### Edge detectors

One-shot pulse on a `BOOL` transition.

- **[`R_TRIG`](r-trig/)** — Rising-edge trigger.
- **[`F_TRIG`](f-trig/)** — Falling-edge trigger.

### Counters

Hold an `INT` count, advanced by edges on the count input.

- **[`CTU`](ctu/)** — Up counter.
- **[`CTD`](ctd/)** — Down counter.
- **[`CTUD`](ctud/)** — Up-and-down counter.

### Timers

Measure elapsed time in `TIME` units.

- **[`TON`](ton/)** — Timer-on-delay.
- **[`TOF`](tof/)** — Timer-off-delay.
- **[`TP`](tp/)** — Pulse timer.

---

## Common patterns

Every standard FB follows the same use pattern:

1. **Declare** an instance variable in the calling POU's `VAR`
   section: `myInstance : <FB_TYPE>;`.
2. **Call** the instance every cycle (or conditionally),
   passing the inputs as named parameters:
   `myInstance(IN := x, PT := T#100ms);`.
3. **Read** the outputs through the instance:
   `IF myInstance.Q THEN ... END_IF;`.

The full pattern with declaration is documented at
[Function and FB calls > FB instances vs. function calls](../../textual/structured-text/function-calls/fb-instance-vs-function/).
