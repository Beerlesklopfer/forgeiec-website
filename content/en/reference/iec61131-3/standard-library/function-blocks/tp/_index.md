---
title: "TP — Pulse timer"
summary: "On the rising edge of IN, Q pulses TRUE for exactly PT, regardless of how long IN stays TRUE."
weight: 25
iec_chapter: "Annex F.7.3"
construct_kind: "function-block"
keywords: ["TP", "timer", "pulse", "PT", "ET", "IN", "Q"]
llm_signals:
  - error_pattern: "TP is a Function Block — declare instance first"
    where: "FStCompiler"
    diagnosis: "TP needs an instance to hold its elapsed counter and the latched edge state."
    fix_strategy: "Declare a TP instance, then call it."
    fix_example: |
      VAR pulseGen : TP; END_VAR
      pulseGen(IN := xTrigger, PT := T#100ms);
      xPulse := pulseGen.Q;
---

## Pin layout

| Direction | Name | Type | Description |
|---|---|---|---|
| Input | `IN` | `BOOL` | Trigger — rising edge starts a pulse |
| Input | `PT` | `TIME` | Pulse duration |
| Output | `Q` | `BOOL` | TRUE for PT after each rising edge of IN |
| Output | `ET` | `TIME` | Elapsed since the pulse started (capped at PT) |

## Semantics

```text
IN goes FALSE → TRUE  : Q := TRUE; ET starts counting from 0
ET reaches PT          : Q := FALSE
IN stays TRUE / FALSE during the pulse: irrelevant — Q is committed for PT
new rising edge while Q is still TRUE: typically ignored (depends on impl);
                                        matiec retriggers the pulse
```

TP differs from TON in that the pulse length is **fixed at
PT**, regardless of how long IN stays TRUE. TP differs from
TOF in that the pulse starts on the **rising** edge, not on
the falling edge.

Common use: hardware-style monostable; a fixed-length
solenoid kick; a "blink one beat" indicator.

## Example

```iec-st
VAR
    pulseLamp : TP;
END_VAR

pulseLamp(IN := xButton, PT := T#500ms);
xLamp := pulseLamp.Q;        (* lamp on for 500 ms after each press *)
```

## IEC reference

IEC 61131-3 third edition (2013), Annex F.7.3.

## matiec conformance

Implemented per the standard. Re-trigger behaviour during an
active pulse is implementation-defined; matiec restarts the
elapsed counter.
