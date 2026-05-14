---
title: "RS — Reset-dominant bistable"
summary: "Set-Reset latch where R1 wins over S in case of conflict. The PLC equivalent of a relay with priority on the reset coil."
weight: 50
iec_chapter: "Annex F.4.2"
construct_kind: "function-block"
keywords: ["RS", "bistable", "set", "reset", "S", "R1", "Q1"]
llm_signals:
  - error_pattern: "RS is a Function Block — declare instance first"
    where: "FStCompiler"
    diagnosis: "RS holds its state Q1 between cycles — that's its entire purpose. Always needs an instance."
    fix_strategy: "Declare an RS instance, then call it."
    fix_example: |
      VAR
          flagLatch : RS;
      END_VAR
      flagLatch(S := xSetCondition, R1 := xResetCondition);
      IF flagLatch.Q1 THEN ... END_IF;
  - error_pattern: "expected 'R1', got 'R'"
    where: "matiec"
    diagnosis: "RS uses pin name R1 (with the digit 1), not R. The 1 marks 'priority input' per IEC convention. SR is symmetric: it uses S1 and R."
    fix_strategy: "Match the pin spelling exactly: RS has S and R1; SR has S1 and R."
    fix_example: |
      (* before — fails *)
      flagLatch(S := xSet, R := xReset);
      (* after *)
      flagLatch(S := xSet, R1 := xReset);
---

## Pin layout

| Direction | Name | Type | Description |
|---|---|---|---|
| Input | `S` | `BOOL` | Set — sets Q1 to TRUE |
| Input | `R1` | `BOOL` | Reset (dominant) — wins over S when both are TRUE |
| Output | `Q1` | `BOOL` | Latched state |

## RS vs. SR

Two flip-flop variants:

| FB | Set input | Reset input | Priority |
|---|---|---|---|
| **RS** | `S` | `R1` | **Reset wins** |
| **SR** | `S1` | `R` | **Set wins** |

The "1" suffix marks the dominant input. Pick **RS** when
safety considerations require that an active reset always
overrides a set request (e.g. emergency-stop systems);
pick **SR** when an active set request must override a
release (e.g. latching alarms).

## Syntax

```iec-st
VAR
    flagLatch : RS;
END_VAR

flagLatch(S := xSetCondition,
          R1 := xResetCondition);

IF flagLatch.Q1 THEN ... END_IF;
```

## Semantics

Per Annex F.4.2, evaluated on each call:

- If `R1 = TRUE`: `Q1 := FALSE` (reset wins).
- Else if `S = TRUE`: `Q1 := TRUE`.
- Else: `Q1` keeps its previous value.

So the truth table:

| S | R1 | Q1 (next) |
|---|---|---|
| F | F | unchanged |
| T | F | TRUE |
| F | T | FALSE |
| T | T | FALSE (R1 wins) |

## When to use RS instead of a plain BOOL

A plain `BOOL` requires explicit assignment whenever the value
should change. An RS encodes the "set on this condition,
reset on that condition" pattern declaratively, which is
clearer than the equivalent IF/ELSIF cascade — and importantly
makes the priority explicit in the FB choice.

```iec-st
(* Equivalent — but reading the FB version, the reset-dominance
   is obvious from the type, no need to inspect the IF order *)
IF xResetCondition THEN
    xLatch := FALSE;
ELSIF xSetCondition THEN
    xLatch := TRUE;
END_IF;

(* vs. RS *)
flagLatch(S := xSetCondition, R1 := xResetCondition);
xLatch := flagLatch.Q1;
```

## IEC reference

IEC 61131-3 third edition (2013), Annex F.4.2 (RS).
The set-dominant SR is in F.4.1.

## matiec conformance

Implemented per the standard. The pin-name spelling (`R1` not
`R`) is the most common LLM mistake — see `llm_signals`.
