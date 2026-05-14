---
title: "FOR loop"
summary: "Counter-driven iteration with explicit start, end, and optional step. Loop variable is implicitly typed by the iteration expressions."
weight: 10
iec_chapter: "6.6.3.4"
construct_kind: "control-flow"
keywords: ["FOR", "TO", "BY", "DO", "END_FOR"]
llm_signals:
  - error_pattern: "Expected END_FOR"
    where: "FStCompiler"
    diagnosis: "FOR block not closed with END_FOR, or a syntax error in the body pushed the parser out of the block."
    fix_strategy: "Add END_FOR; or fix the inner syntax error."
    fix_example: |
      (* before — fails *)
      FOR i := 1 TO 10 DO
          iSum := iSum + arr[i];
      (* after *)
      FOR i := 1 TO 10 DO
          iSum := iSum + arr[i];
      END_FOR;
  - error_pattern: "FOR loop variable type mismatch"
    where: "matiec"
    diagnosis: "The FOR loop variable, the start expression, the end expression and the optional BY step must all share the same IEC integer type. Mixing INT and DINT, or BYTE and INT, fails."
    fix_strategy: "Pick one type for all four (loop var, start, end, BY) and convert the others explicitly."
    fix_example: |
      (* before — fails: i:INT, dwEnd:DINT *)
      FOR i := 1 TO dwEnd DO ... END_FOR;
      (* after *)
      FOR i := 1 TO DINT_TO_INT(dwEnd) DO ... END_FOR;
  - error_pattern: "FOR loop runs forever"
    where: "runtime"
    diagnosis: "The loop never terminates because (a) the BY step is the wrong sign for the direction (e.g. start=1, end=10, step=-1) — IEC allows this and silently never executes; or (b) the body modifies the loop variable in a way that prevents convergence."
    fix_strategy: "Don't modify the loop variable inside the body. Make sure the sign of BY matches the direction (start<end → BY>0; start>end → BY<0)."
    fix_example: |
      (* before — silently runs zero times *)
      FOR i := 10 TO 1 DO ... END_FOR;
      (* after — explicit downward step *)
      FOR i := 10 TO 1 BY -1 DO ... END_FOR;
---

## Syntax

```text
FOR <loop_var> := <start_expr> TO <end_expr> [BY <step_expr>] DO
    <statement_list>
END_FOR;
```

- `<loop_var>` is an existing integer variable. ST does not
  let you declare it inline (unlike C++ `for (int i...`).
- `<start_expr>` and `<end_expr>` must be integer expressions
  of the same type as `<loop_var>`.
- `<step_expr>` is optional; defaults to `+1`. Must be of the
  same type as `<loop_var>` and may be negative.

## Semantics

Per IEC 61131-3 clause 6.6.3.4:

1. Evaluate `<start_expr>`, `<end_expr>`, `<step_expr>`
   **once**. Subsequent changes to those source expressions
   inside the body have no effect on the loop bounds.
2. Set `<loop_var>` to the start value.
3. If `<step_expr> >= 0` and `<loop_var> > <end_expr>`,
   exit. If `<step_expr> < 0` and `<loop_var> < <end_expr>`,
   exit.
4. Run the body.
5. `<loop_var> := <loop_var> + <step_expr>`.
6. Goto step 3.

The loop variable is **not** valid after the loop ends. The
last value depends on the implementation; matiec leaves it
at `end + step`.

## Examples

```iec-st
(* Sum an array *)
iSum := 0;
FOR i := 1 TO 10 DO
    iSum := iSum + arr[i];
END_FOR;

(* Reverse iteration *)
FOR i := 10 TO 1 BY -1 DO
    arr[11 - i] := arr[i];
END_FOR;

(* Skip every second *)
FOR i := 0 TO 100 BY 2 DO
    arrEven[i / 2] := arr[i];
END_FOR;

(* Early exit on found *)
iFound := -1;
FOR i := 0 TO 99 DO
    IF arr[i] = TARGET THEN
        iFound := i;
        EXIT;
    END_IF;
END_FOR;
```

## Scan-cycle warning

A `FOR i := 1 TO 1000 DO` that does substantial work per
iteration easily eats your scan cycle. Cap the loop length
at compile time, profile the body, and split into per-cycle
chunks if needed (use a persistent counter variable that the
POU advances by N per scan).

## IEC reference

IEC 61131-3 third edition (2013), clause **6.6.3.4** — "FOR
statement".

## matiec conformance

matiec implements `FOR` per the standard. The three pitfalls
in `llm_signals` are real and reproducible:

- Type-strict bounds (no auto-promotion).
- Silent zero-iteration when BY sign and start/end direction
  disagree.
- Need for explicit `BY -1` when iterating downward.
