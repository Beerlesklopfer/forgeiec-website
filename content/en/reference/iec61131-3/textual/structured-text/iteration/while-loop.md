---
title: "WHILE loop"
summary: "Pre-test condition. Body runs zero or more times — checked before each iteration."
weight: 20
iec_chapter: "6.6.3.5"
construct_kind: "control-flow"
keywords: ["WHILE", "DO", "END_WHILE"]
llm_signals:
  - error_pattern: "Expected END_WHILE"
    where: "FStCompiler"
    diagnosis: "WHILE block not closed."
    fix_strategy: "Add END_WHILE."
    fix_example: |
      WHILE NOT xDone DO
          DoStep();
      END_WHILE;
  - error_pattern: "WHILE condition must be BOOL"
    where: "matiec"
    diagnosis: "The WHILE condition is not a BOOL — typically an integer expression that 'works' in C-style languages but is illegal in IEC ST."
    fix_strategy: "Convert to an explicit BOOL: `iValue <> 0`, or `iCount > 0`."
    fix_example: |
      (* before — fails *)
      WHILE iCount DO ... END_WHILE;
      (* after *)
      WHILE iCount > 0 DO ... END_WHILE;
  - error_pattern: "task overrun: WHILE never exits"
    where: "runtime"
    diagnosis: "The loop condition never becomes FALSE within one scan cycle. Either the loop body doesn't progress toward the exit condition, or the cycle budget is too small for the work to finish."
    fix_strategy: "Add a safety counter. Cap the iteration count. Or restructure as a step-machine that does one chunk per scan."
    fix_example: |
      (* before — risk of overrun *)
      WHILE NOT xDone DO
          DoStep();
      END_WHILE;
      (* after — bounded *)
      iSafetyCount := 0;
      WHILE NOT xDone AND iSafetyCount < 100 DO
          DoStep();
          iSafetyCount := iSafetyCount + 1;
      END_WHILE;
---

## Syntax

```text
WHILE <bool_expr> DO
    <statement_list>
END_WHILE;
```

## Semantics

1. Evaluate `<bool_expr>`. If `FALSE`, skip the body and
   continue after `END_WHILE`.
2. Run the body.
3. Go to step 1.

The body may run **zero times** if the condition is `FALSE` on
entry. This is the difference from `REPEAT`.

## Examples

```iec-st
(* Drain a queue until empty *)
WHILE iQueueLen > 0 DO
    ProcessOne();
    iQueueLen := iQueueLen - 1;
END_WHILE;

(* Bounded poll *)
iSafetyCount := 0;
WHILE NOT xReady AND iSafetyCount < 50 DO
    DoOneScan();
    iSafetyCount := iSafetyCount + 1;
END_WHILE;
```

## Scan-cycle hazard

`WHILE` without an explicit per-iteration safety counter is a
red flag in PLC code. Even if the body looks bounded, a
runtime data condition (sensor stuck, queue mis-counting)
can keep the loop running until the scan cycle is missed.

Always add an `iSafetyCount` and an upper bound that fits
into your task's CPU budget.

## IEC reference

IEC 61131-3 third edition (2013), clause **6.6.3.5**.

## matiec conformance

Implemented per the standard. The strict BOOL-condition rule
is the main porting pain point from C/Pascal where any
non-zero value is treated as truthy.
