---
title: "IF / ELSIF / ELSE"
summary: "Conditional branching in Structured Text. Evaluates BOOL expressions top-to-bottom and runs the first matching branch."
weight: 10
iec_chapter: "6.6.3.1"
construct_kind: "control-flow"
keywords: ["IF", "THEN", "ELSIF", "ELSE", "END_IF"]
llm_signals:
  - error_pattern: "Expected END_IF"
    where: "FStCompiler"
    diagnosis: "An IF statement was not closed with END_IF, or a nested statement inside an IF/ELSIF branch is malformed and the parser drifted out of the IF block before reaching END_IF."
    fix_strategy: "Add the missing END_IF; or fix the syntax error that the parser actually tripped on first (often a missing semicolon or an undeclared identifier)."
    fix_example: |
      (* before — fails: Expected END_IF *)
      IF iStep = 0 THEN
          bMask := 1
      (* after — compiles *)
      IF iStep = 0 THEN
          bMask := 1;
      END_IF;
  - error_pattern: "Unexpected token: 'ELSIF'"
    where: "FStCompiler"
    diagnosis: "ELSIF spelled differently (e.g. ELSEIF, ELIF) — IEC 61131-3 mandates the four-letter ELSIF form."
    fix_strategy: "Replace ELSEIF / ELIF with ELSIF."
    fix_example: |
      (* before — fails *)
      IF a THEN x:=1; ELSEIF b THEN x:=2; END_IF;
      (* after — compiles *)
      IF a THEN x:=1; ELSIF b THEN x:=2; END_IF;
  - error_pattern: "comparison of integer expressions of different types"
    where: "matiec"
    diagnosis: "The IF condition compares variables of different IEC types (e.g. INT vs UINT, BYTE vs INT). matiec is strict about implicit conversions and rejects the implicit promotion."
    fix_strategy: "Add an explicit type-conversion call (INT_TO_UINT, UINT_TO_INT, BYTE_TO_INT, ...) on one of the operands so the comparison happens in a single type."
    fix_example: |
      (* before — fails: comparison of integer expressions of different types *)
      IF iStep = bMask THEN ... END_IF;   (* iStep INT, bMask BYTE *)
      (* after — compiles *)
      IF iStep = BYTE_TO_INT(bMask) THEN ... END_IF;
---

## Definition

Conditional branching: evaluate a `BOOL` expression and, if it
is `TRUE`, run the statements between `THEN` and the next
`ELSIF` / `ELSE` / `END_IF`. Up to one `ELSIF` block per
extra condition; up to one optional `ELSE` block as the final
catch-all.

The `IF` statement always commits to **exactly one** branch.
The first `THEN` whose condition evaluates `TRUE` wins; later
`ELSIF` conditions are not even evaluated.

## Syntax

```text
IF <bool_expr> THEN
    <statement_list>
[ELSIF <bool_expr> THEN
    <statement_list>]*
[ELSE
    <statement_list>]
END_IF;
```

`<bool_expr>` evaluates to a single `BOOL`. Both branches'
`<statement_list>` may be empty.

### Example

```iec-st
(* Bit-mask lookup by step index — see CASE-statement for the
   alternative spelling. *)
IF iStep = 0 THEN
    bMask := INT_TO_BYTE(1);
ELSIF iStep = 1 THEN
    bMask := INT_TO_BYTE(2);
ELSIF iStep = 2 THEN
    bMask := INT_TO_BYTE(4);
ELSE
    bMask := INT_TO_BYTE(0);
END_IF;
```

## Semantics

Conditions evaluate left-to-right, top-to-bottom. As soon as
one condition returns `TRUE`, that branch's statement list runs
and execution leaves the `IF` block. No fall-through. If no
condition is `TRUE` and no `ELSE` branch exists, the `IF`
block is a no-op.

`BOOL` is a real two-valued type, not a numeric tested for
non-zero. `IF iCounter THEN …` is a type error in IEC 61131-3
even though many vendor-specific dialects accept it.

## IEC reference

IEC 61131-3 third edition (2013), clause **6.6.3.1** — "IF
statement". The keywords `IF`, `THEN`, `ELSIF`, `ELSE`,
`END_IF` are reserved.

## matiec conformance

matiec implements `IF` / `ELSIF` / `ELSE` exactly as the
standard requires. No known emit-bugs.

The strict typing rule is enforced more aggressively than some
operators: `IF a = b THEN …` with `a: INT` and `b: UINT` will
fail at the matiec layer (after the local FStCompiler accepts
it). Always wrap one side in the explicit conversion call —
see `comparison of integer expressions of different types` in
the `llm_signals` block.

## ForgeIEC notes

- ForgeIEC's editor highlights `THEN` / `ELSIF` / `ELSE` /
  `END_IF` via tree-sitter (Memory: `feedback_treesitter_rename_refactor`).
- A nested IF that crosses task boundaries is not special — the
  IF runs entirely within one task cycle.
- For repetitive multi-way dispatch on a single integer
  expression, prefer [`CASE`](../case-statement/) over a long
  `ELSIF` cascade. The IF cascade exists because matiec has
  emit-bugs with certain `CASE`-list literal forms (see the
  `CASE` page); when the inputs are clean, `CASE` reads
  better.
