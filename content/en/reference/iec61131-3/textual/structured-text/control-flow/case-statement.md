---
title: "CASE / OF / ELSE / END_CASE"
summary: "Multi-way dispatch on an integer-valued expression. Each case label or label-range selects one branch."
weight: 20
iec_chapter: "6.6.3.2"
construct_kind: "control-flow"
keywords: ["CASE", "OF", "ELSE", "END_CASE"]
llm_signals:
  - error_pattern: "Unexpected token: '01'"
    where: "FStCompiler"
    diagnosis: "matiec's lexer misreads the typed-hex literal `16#01` inside a CASE-OF case label. It tokenises `16#` as a type prefix and then chokes on the bare `01` digits before it can fold them back into a single integer literal."
    fix_strategy: "Replace hexadecimal literals in CASE case labels with their decimal equivalents (16#01 → 1, 16#02 → 2, 16#04 → 4, 16#08 → 8, 16#10 → 16, 16#20 → 32). The right-hand side of the case body can keep hex; only the case label itself is affected."
    fix_example: |
      (* before — fails: Unexpected token: '01' *)
      CASE iStep OF
          0: bMask := 16#01;
          1: bMask := 16#02;
      END_CASE;
      (* after — compiles. Note the assignment can stay decimal too;
         BYTE assignment from INT widens implicitly. *)
      CASE iStep OF
          0: bMask := INT_TO_BYTE(1);
          1: bMask := INT_TO_BYTE(2);
      END_CASE;
  - error_pattern: "Expected END_CASE"
    where: "FStCompiler"
    diagnosis: "A CASE block was not closed with END_CASE, or one of the case-bodies has a syntax error that pushed the parser out of the block early."
    fix_strategy: "Add the missing END_CASE; or fix the first inner syntax error (commonly missing semicolon, or an unclosed nested IF)."
    fix_example: |
      (* before *)
      CASE iStep OF
          0: bMask := 1;
          1: bMask := 2
      END_CASE;
      (* after — semicolon was missing after `bMask := 2` *)
      CASE iStep OF
          0: bMask := 1;
          1: bMask := 2;
      END_CASE;
  - error_pattern: "case label .* not in scrutinee type"
    where: "matiec"
    diagnosis: "The case scrutinee (the expression after CASE) and the case labels are different IEC types. Common variant: scrutinee is INT, labels are BYTE literals (e.g. `BYTE#1`)."
    fix_strategy: "Either change the scrutinee's type, or write the labels as integer constants of the scrutinee's type. Untyped integer literals (1, 2, 3) are widened by matiec to match the scrutinee."
    fix_example: |
      (* before — fails because BYTE#1 doesn't match INT iStep *)
      CASE iStep OF
          BYTE#1: bMask := 2;
      END_CASE;
      (* after — bare integer literal coerces to scrutinee type *)
      CASE iStep OF
          1: bMask := 2;
      END_CASE;
---

## Definition

Multi-way dispatch on an integer-valued expression (the
*scrutinee*). The body lists one or more case-labels followed
by a colon and a statement-list; the scrutinee value is matched
against each label and the first matching branch runs. An
optional `ELSE` branch is the catch-all.

Case labels may be:
- A single value (`5:`),
- A list of values (`1, 3, 5:`),
- A range of values (`1..10:`),
- Any combination of the above (`1, 3, 5..10:`).

Case labels MUST be unique across the whole `CASE` block; the
scrutinee MUST be of an integer type (`SINT`, `INT`, `DINT`,
`LINT` and their unsigned variants); labels MUST be compile-
time constant expressions of an integer type compatible with
the scrutinee.

## Syntax

```text
CASE <int_expr> OF
    <label_list_1>:
        <statement_list_1>
    [<label_list_n>:
        <statement_list_n>]*
[ELSE
    <statement_list_else>]
END_CASE;
```

### Example

```iec-st
(* Bit-mask lookup by step index. CASE reads cleaner than a
   long IF/ELSIF cascade for purely numeric dispatch. Note the
   plain decimal literals on the right-hand side — see the
   matiec-quirk warning above. *)
CASE iStep OF
    0: bMask := INT_TO_BYTE(1);
    1: bMask := INT_TO_BYTE(2);
    2: bMask := INT_TO_BYTE(4);
    3: bMask := INT_TO_BYTE(8);
    4: bMask := INT_TO_BYTE(16);
    5: bMask := INT_TO_BYTE(32);
ELSE
    bMask := INT_TO_BYTE(0);
END_CASE;
```

## Semantics

The scrutinee is evaluated **once**. The branches are scanned
top-to-bottom; the first label-list that contains the
scrutinee value wins. Label-list overlap is forbidden by the
standard, but matiec only catches obvious overlaps (the same
literal in two label lists). Numeric ranges are inclusive on
both ends (`1..3` matches 1, 2, 3).

If no label matches and no `ELSE` branch exists, the `CASE`
block is a no-op.

## IEC reference

IEC 61131-3 third edition (2013), clause **6.6.3.2** — "CASE
statement". Keywords `CASE`, `OF`, `ELSE`, `END_CASE` are
reserved.

## matiec conformance

Two known quirks worth flagging up front:

**Hex literal in case labels** (see `llm_signals` above). matiec's
front-end lexer mis-tokenises `16#01` when it appears as a
case label. The diagnostic is the unhelpful `Unexpected token: '01'`.
Workaround: use decimal labels (`1`, `2`, `4`, …) — bare integer
literals widen to the scrutinee's type implicitly.

**Bit-shift via `SHL` in case bodies** is unrelated to `CASE`
itself but co-occurs frequently because both come up in
bit-mask code. matiec emits broken C for
`SHL(BYTE#1, INT_TO_UINT(x))` (it generates a `data__->BYTE`
struct-member access for the typed-literal). Avoid `SHL` in
matiec; do the dispatch with `CASE` (this page) or `IF/ELSIF`
([../if-statement/](../if-statement/)) and a literal table.

## ForgeIEC notes

The Ackersteuerung example project (2026-05-14 cleanup, see
`project_ackersteuerung_save_load_bug` memory) hits both quirks
in one place: `FB_MANUAL_TIME` originally used
`SHL(BYTE#1, iMtStep)` to compute a per-step bit-mask. After
`SHL` was rejected by matiec the natural rewrite to `CASE OF`
with hex labels then hit the `Unexpected token: '01'` quirk on
`16#01`. The working form (currently in production):

```iec-st
IF iMtStep = 0 THEN
    bMtMask := INT_TO_BYTE(1);
ELSIF iMtStep = 1 THEN
    bMtMask := INT_TO_BYTE(2);
ELSIF iMtStep = 2 THEN
    bMtMask := INT_TO_BYTE(4);
ELSIF iMtStep = 3 THEN
    bMtMask := INT_TO_BYTE(8);
ELSIF iMtStep = 4 THEN
    bMtMask := INT_TO_BYTE(16);
ELSIF iMtStep = 5 THEN
    bMtMask := INT_TO_BYTE(32);
ELSE
    bMtMask := INT_TO_BYTE(0);
END_IF;
```

The same logic in pure `CASE` works once the labels are
decimal, but the `IF/ELSIF` cascade is what is currently
deployed and in scan-cycle.
