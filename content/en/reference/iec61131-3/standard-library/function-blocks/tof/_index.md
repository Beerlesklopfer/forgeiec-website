---
title: "TOF — Timer-Off-Delay"
summary: "Q follows IN going TRUE immediately; stays TRUE for PT after IN returns to FALSE."
weight: 20
iec_chapter: "Annex F.7.2"
construct_kind: "function-block"
keywords: ["TOF", "timer", "off-delay", "PT", "ET", "IN", "Q"]
llm_signals:
  - error_pattern: "TOF is a Function Block — declare instance first"
    where: "FStCompiler"
    diagnosis: "TOF is an FB; needs an instance to hold its elapsed counter."
    fix_strategy: "Declare a TOF instance, then call it."
    fix_example: |
      VAR releaseDelay : TOF; END_VAR
      releaseDelay(IN := xLevelOk, PT := T#5s);
      IF NOT releaseDelay.Q THEN xValve := FALSE; END_IF;
---

## Pin layout

| Direction | Name | Type | Description |
|---|---|---|---|
| Input | `IN` | `BOOL` | Drives Q TRUE on rising edge; starts the off-delay on falling edge |
| Input | `PT` | `TIME` | How long Q stays TRUE after IN returns to FALSE |
| Output | `Q` | `BOOL` | TRUE while IN is TRUE OR within PT after IN's last falling edge |
| Output | `ET` | `TIME` | Elapsed since IN's last falling edge (0 while IN is TRUE) |

## Semantics

```text
IN goes FALSE → TRUE  : Q := TRUE; ET := T#0s
IN stays TRUE         : Q stays TRUE; ET stays at 0
IN goes TRUE → FALSE  : start counting ET
ET reaches PT          : Q := FALSE
IN goes FALSE → TRUE again before PT : Q stays TRUE; ET reset
```

TOF is the symmetric opposite of TON: TON delays the **rising
edge** of Q, TOF delays the **falling edge**.

Common use: drag-out time on a pump after a sensor signal
disappears, debounce of a falling level, "stay armed for X
seconds after the trigger releases".

## Example

```iec-st
VAR
    releaseDelay : TOF;
END_VAR

releaseDelay(IN := xLevelOk, PT := T#5s);

(* Q is TRUE while xLevelOk is TRUE, AND for 5s after it goes FALSE *)
xPump := releaseDelay.Q;
```

## IEC reference

IEC 61131-3 third edition (2013), Annex F.7.2.

## matiec conformance

Implemented per the standard.
