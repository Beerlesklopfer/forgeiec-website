---
title: "CTU — Counter-Up"
summary: "INT counter that increments on each rising edge of CU.Q goes TRUE when CV reaches the preset PV."
weight: 30
iec_chapter: "Annex F.6.1"
construct_kind: "function-block"
keywords: ["CTU", "counter", "CU", "PV", "CV", "Q", "R"]
llm_signals:
  - error_pattern: "CTU is a Function Block — declare instance first"
    where: "FStCompiler"
    diagnosis: "CTU is being called directly. Like all FBs it needs an instance to hold the count between scan cycles."
    fix_strategy: "Declare a CTU instance, then call the instance."
    fix_example: |
      VAR
          ctrPulse : CTU;
      END_VAR
      ctrPulse(CU := xButton, R := xReset, PV := 10);
      IF ctrPulse.Q THEN ... END_IF;
  - error_pattern: "CTU never increments"
    where: "runtime"
    diagnosis: "CTU counts on the **rising edge** of CU. If CU stays continuously TRUE, no further counts happen — the FB needs to see CU drop to FALSE and rise to TRUE to increment."
    fix_strategy: "Make sure CU is pulsed (e.g. driven by an R_TRIG or naturally edge-shaped). For an always-counting timer, use a TON whose Q is fed back to its own IN through a NOT — that produces a rising edge per cycle of the period."
    fix_example: |
      (* before — CU stays TRUE forever, counter never advances *)
      ctrPulse(CU := TRUE, R := xReset, PV := 10);
      (* after — pulse via R_TRIG *)
      VAR
          edgeRise : R_TRIG;
          ctrPulse : CTU;
      END_VAR
      edgeRise(CLK := xButton);
      ctrPulse(CU := edgeRise.Q, R := xReset, PV := 10);
---

## Pin layout

| Direction | Name | Type | Description |
|---|---|---|---|
| Input | `CU` | `BOOL` | Count Up — increment CV on each rising edge |
| Input | `R` | `BOOL` | Reset — when TRUE, CV is forced to 0 |
| Input | `PV` | `INT` | Preset Value — Q fires when CV >= PV |
| Output | `Q` | `BOOL` | TRUE when CV >= PV |
| Output | `CV` | `INT` | Current Value — the running count |

## Syntax

```iec-st
VAR
    ctrPulse : CTU;
END_VAR

ctrPulse(CU := xPulse,
         R  := xReset,
         PV := 10);

IF ctrPulse.Q THEN ... END_IF;
iCurrent := ctrPulse.CV;
```

## Semantics

Per Annex F.6.1, evaluated on each call:

- If `R = TRUE`: `CV := 0`. (Reset has priority.)
- Else if `CU` rose from `FALSE` to `TRUE` since the last call:
  `CV := CV + 1` (saturates at INT max).
- `Q := (CV >= PV)`.

**`CU` triggers on the rising edge.** A CU that stays
continuously `TRUE` produces exactly one increment (on the
first call after the rise). To count cyclic events you need a
real edge — either from hardware (button presses) or from an
R_TRIG / TON-feedback pattern in software.

## IEC reference

IEC 61131-3 third edition (2013), Annex F.6.1.

## matiec conformance

Implemented per the standard. The "CU stays TRUE → no
increments" semantic is per-spec, not a bug — but it's a
common LLM trap (see `llm_signals`).
