---
title: "F_TRIG — Falling-edge trigger"
summary: "One-cycle pulse on a BOOL going from TRUE to FALSE. The mirror of R_TRIG."
weight: 45
iec_chapter: "Annex F.5.2"
construct_kind: "function-block"
keywords: ["F_TRIG", "edge", "falling", "CLK", "Q"]
llm_signals:
  - error_pattern: "F_TRIG is a Function Block — declare instance first"
    where: "FStCompiler"
    diagnosis: "F_TRIG holds the previous CLK between cycles."
    fix_strategy: "Declare an F_TRIG instance, call it every cycle."
---

## Pin layout

| Direction | Name | Type | Description |
|---|---|---|---|
| Input | `CLK` | `BOOL` | Signal to edge-detect |
| Output | `Q` | `BOOL` | TRUE for one scan after CLK falls TRUE→FALSE |

## Semantics

```text
Q := NOT CLK AND _previousCLK
_previousCLK := CLK
```

Internal `_previousCLK` starts as `FALSE`. So the first call
where `CLK = TRUE` does **not** fire Q (no previous TRUE),
but the next call where `CLK = FALSE` while `_previousCLK =
TRUE` fires Q for one scan.

## Example

```iec-st
VAR
    edgeFall : F_TRIG;
END_VAR

edgeFall(CLK := xButton);

IF edgeFall.Q THEN
    DoOnRelease();
END_IF;
```

Symmetric to [R_TRIG](../r-trig/) — same usage pattern, only
the edge direction differs.

## IEC reference

IEC 61131-3 third edition (2013), Annex F.5.2.

## matiec conformance

Implemented per the standard.
