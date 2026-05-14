---
title: "REPEAT loop"
summary: "Post-test condition. Body always runs at least once; UNTIL condition is checked at the end of each iteration."
weight: 30
iec_chapter: "6.6.3.6"
construct_kind: "control-flow"
keywords: ["REPEAT", "UNTIL", "END_REPEAT"]
llm_signals:
  - error_pattern: "Expected END_REPEAT"
    where: "FStCompiler"
    diagnosis: "REPEAT block not closed."
    fix_strategy: "Add END_REPEAT after the UNTIL clause."
    fix_example: |
      REPEAT
          DoStep();
      UNTIL xDone
      END_REPEAT;
  - error_pattern: "Expected UNTIL"
    where: "FStCompiler"
    diagnosis: "REPEAT body lacks the UNTIL clause. REPEAT requires an UNTIL exit condition; without it the parser fails before reaching END_REPEAT."
    fix_strategy: "Add the UNTIL <bool_expr> clause."
    fix_example: |
      (* before — fails *)
      REPEAT
          DoStep();
      END_REPEAT;
      (* after *)
      REPEAT
          DoStep();
      UNTIL xDone
      END_REPEAT;
---

## Syntax

```text
REPEAT
    <statement_list>
UNTIL <bool_expr>
END_REPEAT;
```

Note no `;` after `<bool_expr>` in the IEC standard — `END_REPEAT` 
follows directly. matiec accepts both forms.

## Semantics

1. Run the body.
2. Evaluate `<bool_expr>`. If `TRUE`, exit. If `FALSE`,
   go to step 1.

The body **always runs at least once**, in contrast with
`WHILE`. Use `REPEAT` when you need to do something at least
once before checking whether to continue.

## REPEAT vs. WHILE

| Question | Use |
|---|---|
| "Run while X is true (might run zero times)" | `WHILE x DO ... END_WHILE` |
| "Run until X becomes true (always at least once)" | `REPEAT ... UNTIL x END_REPEAT` |

The condition direction is flipped: `WHILE` continues while
the condition is `TRUE`; `REPEAT` continues until the
condition becomes `TRUE`.

## Example

```iec-st
(* Read until end-of-data marker *)
REPEAT
    iValue := ReadNext();
    arr[iIndex] := iValue;
    iIndex := iIndex + 1;
UNTIL iValue = SENTINEL
END_REPEAT;
```

The same scan-cycle warning as `WHILE` applies — bound the
loop with a safety counter if the exit condition depends on
external data.

## IEC reference

IEC 61131-3 third edition (2013), clause **6.6.3.6**.

## matiec conformance

Implemented per the standard.
