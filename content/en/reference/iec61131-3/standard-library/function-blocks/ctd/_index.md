---
title: "CTD — Counter-Down"
summary: "INT counter that decrements on each rising edge of CD. Q goes TRUE when CV reaches 0."
weight: 35
iec_chapter: "Annex F.6.2"
construct_kind: "function-block"
keywords: ["CTD", "counter", "down", "CD", "PV", "CV", "Q", "LD"]
llm_signals:
  - error_pattern: "CTD is a Function Block — declare instance first"
    where: "FStCompiler"
    diagnosis: "Standard FB declaration rule applies."
    fix_strategy: "Declare a CTD instance, call the instance."
---

## Pin layout

| Direction | Name | Type | Description |
|---|---|---|---|
| Input | `CD` | `BOOL` | Count Down — decrement CV on each rising edge |
| Input | `LD` | `BOOL` | Load — when TRUE, set CV := PV |
| Input | `PV` | `INT` | Preset Value loaded by LD |
| Output | `Q` | `BOOL` | TRUE when CV <= 0 |
| Output | `CV` | `INT` | Current Value |

## Semantics

```text
LD = TRUE  : CV := PV
CD rising  : CV := CV - 1 (saturates at INT min)
Q := CV <= 0
```

LD has priority over CD. Use LD to (re-)initialise the
counter to its preset.

## Example

```iec-st
VAR
    countdown : CTD;
END_VAR

countdown(CD := xPulse, LD := xReset, PV := 10);

IF countdown.Q THEN
    (* zero reached *)
    DoFinish();
END_IF;
```

## IEC reference

IEC 61131-3 third edition (2013), Annex F.6.2.

## matiec conformance

Implemented per the standard. Same edge-detection caveat as
CTU: CD must see a real rising edge per increment.
