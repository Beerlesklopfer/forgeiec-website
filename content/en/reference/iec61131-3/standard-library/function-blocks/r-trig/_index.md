---
title: "R_TRIG — Rising-edge trigger"
summary: "Single-cycle pulse on a BOOL going from FALSE to TRUE. The bread-and-butter way to convert a level signal into an edge event."
weight: 40
iec_chapter: "Annex F.5.1"
construct_kind: "function-block"
keywords: ["R_TRIG", "edge", "rising", "CLK", "Q", "trigger"]
llm_signals:
  - error_pattern: "R_TRIG is a Function Block — declare instance first"
    where: "FStCompiler"
    diagnosis: "R_TRIG keeps the previous CLK value between cycles — that's why it's an FB and needs an instance."
    fix_strategy: "Declare an R_TRIG instance, then call it."
    fix_example: |
      VAR
          edgeRise : R_TRIG;
      END_VAR
      edgeRise(CLK := xButton);
      IF edgeRise.Q THEN ... END_IF;
  - error_pattern: "R_TRIG.Q never fires"
    where: "runtime"
    diagnosis: "Most likely (a) CLK was already TRUE on the very first call (no rising edge to detect — the previous value defaults to FALSE so the first TRUE-on-call typically fires unless the FB was created mid-cycle); or (b) you're checking Q without calling the instance every cycle."
    fix_strategy: "Call the instance unconditionally every scan — that's how it can compare 'this CLK' to 'last CLK'. Don't gate the call on the very signal you want to edge-detect."
    fix_example: |
      (* before — call only when xButton is TRUE → no edge ever detected *)
      IF xButton THEN
          edgeRise(CLK := xButton);
          IF edgeRise.Q THEN ... END_IF;
      END_IF;
      (* after — call every cycle, gate behaviour on Q *)
      edgeRise(CLK := xButton);
      IF edgeRise.Q THEN ... END_IF;
---

## Pin layout

| Direction | Name | Type | Description |
|---|---|---|---|
| Input | `CLK` | `BOOL` | Signal to edge-detect |
| Output | `Q` | `BOOL` | TRUE for exactly one scan after CLK rises FALSE→TRUE |

## Syntax

```iec-st
VAR
    edgeRise : R_TRIG;
END_VAR

edgeRise(CLK := xButton);

IF edgeRise.Q THEN
    iCounter := iCounter + 1;
END_IF;
```

## Semantics

Per Annex F.5.1, evaluated on each call:

- `Q := CLK AND NOT _previousCLK`.
- `_previousCLK := CLK`.

The internal `_previousCLK` starts as `FALSE` on instance
creation. So the first call where `CLK = TRUE` produces a
rising edge regardless of how `CLK` looked outside the
program — useful for one-shot startup actions.

## Why edge detection at all?

PLC scan cycles often see the same level signal `TRUE` for
many consecutive cycles. If you want "do X **once** when the
button is pressed", you can't just write
`IF xButton THEN DoX(); END_IF;` because that fires `DoX()`
every scan while the button is held down.

R_TRIG turns the level into an event:

```iec-st
edgeRise(CLK := xButton);
IF edgeRise.Q THEN
    DoX();   (* fires exactly once per press *)
END_IF;
```

## IEC reference

IEC 61131-3 third edition (2013), Annex F.5.1.

## matiec conformance

Implemented per the standard. The instance-must-live-across-
cycles requirement (and therefore the FB nature) is the most
common LLM trap — `R_TRIG(CLK := x)` directly is a compile
error; only `myEdge(CLK := x)` works.
