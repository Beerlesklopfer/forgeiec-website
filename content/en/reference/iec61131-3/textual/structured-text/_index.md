---
title: "Structured Text (ST)"
summary: "ForgeIEC's primary PLC programming language. Pascal-like, statement-oriented, strongly typed."
weight: 30
---

## Structured Text

Structured Text is the language ForgeIEC uses by default for new
POUs. Syntax is Pascal-derived: assignment is `:=`, statements
end with `;`, control-flow keywords are spelled out (`IF`,
`THEN`, `ELSIF`, `ELSE`, `END_IF`), and types are declared
separately from values.

This chapter covers every ST construct that ForgeIEC accepts.
Pages are organised by syntactic category, mirroring the IEC
61131-3 third edition section ordering for ST (clause 6.6 in the
2013 edition).

---

## Sections

### Literals

Numeric constants (integer, real, time, duration, date), bit
strings, character strings, typed literals (`BYTE#1`, `INT#42`,
`T#100ms`).

- [Integer & hexadecimal literals](literals/integer-literals/)
  — `1`, `42`, `16#FF`, `BYTE#1`, `INT#-3`, plus the matiec
  emit-bug with typed hex inside `CASE` case lists.

### [Operators](operators/)

Arithmetic, bitwise, comparison and assignment operators with
precedence and operand-type rules. matiec is strict on type
matching — most ported code from C / Codesys / B&R needs
explicit conversion calls inserted.

- [Arithmetic](operators/arithmetic/) — `+`, `-`, `*`, `/`, `MOD`, `**`.
- [Bitwise & logical](operators/bitwise/) — `AND`, `OR`, `XOR`, `NOT`.
- [Comparison](operators/comparison/) — `=`, `<>`, `<`, `<=`, `>`, `>=`.
- [Assignment & precedence](operators/assignment-and-precedence/)
  — `:=` and the full precedence table.

### [Variables and references](variables-references/)

How identifiers resolve in ST. Includes ForgeIEC's
three-namespace pool model (`Anvil.<Device>.<Var>`,
`Bellows.<Group>.<Var>`, `GVL.<Namespace>.<Var>`) plus member
access, bit access, array indexing.

### [Function and FB calls](function-calls/)

Two different mechanisms — Functions (FUN) are called directly,
Function Blocks (FBs) need an instance declaration first. Most
common LLM compile-error source in ForgeIEC.

- [FB instances vs. function calls](function-calls/fb-instance-vs-function/)
  — *"X is a Function Block — declare instance first"* and
  the canonical TON / CTU / R_TRIG declaration pattern.
- [Positional vs. named parameters](function-calls/positional-vs-named/)
  — *"has no declared parameter list"* and when to prefer which
  call form.

### Control flow

How execution proceeds through the body of a POU.

- [`IF` / `ELSIF` / `ELSE`](control-flow/if-statement/)
  — conditional branching.
- [`CASE`](control-flow/case-statement/)
  — multi-way dispatch on integer expressions, including the
  matiec emit-bug with `SHL(BYTE#1, …)` and the literal-type
  pitfall in case lists.

### [Iteration (loops)](iteration/)

Three loop forms plus the scan-cycle hazard discussion (loops
on a PLC must be bounded — they block the cycle).

- [`FOR`](iteration/for-loop/) — counter-driven iteration.
- [`WHILE`](iteration/while-loop/) — pre-test condition.
- [`REPEAT`](iteration/repeat-loop/) — post-test condition.

### [Selection and jump](selection-and-jump/)

`RETURN`, `EXIT`, `CONTINUE` plus the deprecated/removed
`GOTO` and its modern replacements.

---

## ForgeIEC-specific reference rules

ForgeIEC adds three reference forms on top of the IEC standard
that are worth keeping in mind while reading the per-construct
pages:

- **`Anvil.<Device>.<Var>`** — a bus-bound pool variable. The
  middle segment is the device hostname (= AnvilVarList POU
  name).
- **`Bellows.<Group>.<Var>`** — a pool variable that carries
  `bellowsExport=true` and is mirrored by the Bellows OPC-UA /
  Modbus-TCP gateway. Same physical pool entry as the matching
  `Anvil.*` form (dual-namespace alias) when both apply.
- **`GVL.<Namespace>.<Var>`** — a plain global variable
  (`VAR_GLOBAL`, no special binding).

POU-local variables are referenced by their bare name without
prefix. The ForgeIEC ST resolver matches case-insensitively per
IEC 61131-3 §1.4.2.
