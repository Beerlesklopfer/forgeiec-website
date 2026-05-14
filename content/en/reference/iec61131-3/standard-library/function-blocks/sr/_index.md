---
title: "SR — Set-dominant bistable"
summary: "Set-Reset latch where S1 wins over R. The set-dominant counterpart of RS."
weight: 55
iec_chapter: "Annex F.4.1"
construct_kind: "function-block"
keywords: ["SR", "bistable", "set", "reset", "S1", "R", "Q1"]
llm_signals:
  - error_pattern: "SR is a Function Block — declare instance first"
    where: "FStCompiler"
    diagnosis: "SR holds Q1 between cycles."
    fix_strategy: "Declare an SR instance, call it."
  - error_pattern: "expected 'S1', got 'S'"
    where: "matiec"
    diagnosis: "SR uses pin name S1 (with the digit 1) for the dominant input. Mirror of RS, which uses R1."
    fix_strategy: "Match the pin spelling: SR has S1 + R; RS has S + R1."
---

## Pin layout

| Direction | Name | Type | Description |
|---|---|---|---|
| Input | `S1` | `BOOL` | Set (dominant) — wins over R when both are TRUE |
| Input | `R` | `BOOL` | Reset |
| Output | `Q1` | `BOOL` | Latched state |

## SR vs. RS

| FB | Set input | Reset input | Priority |
|---|---|---|---|
| **SR** (this page) | `S1` | `R` | **Set wins** |
| **[RS](../rs/)** | `S` | `R1` | **Reset wins** |

The "1" suffix marks the dominant input. Pick **SR** when an
active set request must override a release (latching alarms,
fault counters that should remember their trip until manual
acknowledge); pick **RS** when an active reset must override
a set (safety-stop systems).

## Semantics

```text
S1 = TRUE  : Q1 := TRUE  (set wins)
R = TRUE   : Q1 := FALSE (only when S1 = FALSE)
both FALSE : Q1 unchanged
```

Truth table:

| S1 | R | Q1 (next) |
|---|---|---|
| F | F | unchanged |
| T | F | TRUE |
| F | T | FALSE |
| T | T | TRUE (S1 wins) |

## Example

```iec-st
VAR
    alarmLatch : SR;
END_VAR

alarmLatch(S1 := xFaultCondition,
           R  := xOperatorAck);

IF alarmLatch.Q1 THEN
    xAlarmLamp := TRUE;
END_IF;
```

Latching alarms are the canonical SR use-case: a fault that
self-clears (sensor recovers) should keep the alarm on until
the operator acknowledges. SR encodes "set on fault, only
release on ack" with set-priority by construction.

## IEC reference

IEC 61131-3 third edition (2013), Annex F.4.1.

## matiec conformance

Implemented per the standard.
