---
title: "Integer & hexadecimal literals"
summary: "Decimal, binary, octal, hexadecimal integer constants and their typed (BYTE#1, INT#-3, …) variants."
weight: 10
iec_chapter: "6.3.1"
construct_kind: "literal"
keywords: ["integer", "literal", "hex", "16#", "BYTE#", "INT#", "DINT#", "UINT#"]
llm_signals:
  - error_pattern: "Unexpected token: '01'"
    where: "FStCompiler"
    diagnosis: "Typed-hex literal `16#01` (or any 16#xx) used as a CASE-OF case label. matiec's lexer parses `16#` as a type prefix and then chokes on the digits before they are folded back into a single integer literal. The same expression is fine on the right-hand side of an assignment; only the case-label slot triggers it."
    fix_strategy: "Switch to decimal literals in case labels (16#01 → 1, 16#02 → 2, 16#04 → 4, 16#08 → 8, 16#10 → 16, 16#20 → 32). Hex literals on the right-hand side of `:=` stay as-is. See the [CASE statement](../control-flow/case-statement/) page for the full pattern."
    fix_example: |
      (* before — fails: Unexpected token: '01' *)
      CASE iStep OF
          0: bMask := 16#01;
          1: bMask := 16#02;
      END_CASE;
      (* after — compiles *)
      CASE iStep OF
          0: bMask := INT_TO_BYTE(1);
          1: bMask := INT_TO_BYTE(2);
      END_CASE;
  - error_pattern: "'BYTE' has no member named 'BYTE'"
    where: "gcc"
    diagnosis: "matiec emits `data__->BYTE` instead of a literal cast when it sees `BYTE#1` as a function-call argument (e.g. inside `SHL(BYTE#1, …)`). The g++ compile pass on the PLC then fails because there is no struct member called `BYTE`. The bug is in matiec's C-generator's handling of typed literals as arguments."
    fix_strategy: "Don't use typed-literal-as-argument syntax with matiec. Pass an explicit conversion call instead: `INT_TO_BYTE(1)`, `INT_TO_UINT(x)`, etc. Or remove the typed literal entirely if the surrounding expression doesn't need the explicit type — bare integer literals widen by IEC promotion rules."
    fix_example: |
      (* before — local FStCompiler accepts, gcc fails *)
      bMask := SHL(BYTE#1, INT_TO_UINT(iStep));
      (* after — pre-compute the mask in plain ST *)
      IF iStep = 0 THEN bMask := INT_TO_BYTE(1);
      ELSIF iStep = 1 THEN bMask := INT_TO_BYTE(2);
      (* ... *)
      END_IF;
  - error_pattern: "integer constant out of range"
    where: "matiec"
    diagnosis: "An untyped integer literal exceeds the range of the type it is being used with, e.g. `bMask := 256;` where `bMask: BYTE` (max 255)."
    fix_strategy: "Either pick a wider type for the variable (`bMask: WORD` for 0..65535), or make the literal an exact match for the variable's range. Never silently truncate."
    fix_example: |
      (* before — fails *)
      bMask : BYTE; bMask := 256;
      (* after — option A: widen the variable *)
      bMask : WORD; bMask := 256;
      (* after — option B: keep BYTE, pick valid value *)
      bMask : BYTE; bMask := 128;
---

## Definition

Integer literals denote a single integer value. Four bases are
defined by the standard:

| Base | Prefix | Example | Decimal value |
|------|--------|---------|---------------|
| Decimal | (none) | `42` | 42 |
| Binary | `2#` | `2#1010` | 10 |
| Octal | `8#` | `8#52` | 42 |
| Hexadecimal | `16#` | `16#2A` | 42 |

Underscores between digits are allowed for readability and have
no semantic effect: `1_000_000`, `2#1010_1100`. A leading `+`
or `-` sign turns the literal into a signed value. Hexadecimal
digits are case-insensitive (`16#FF` = `16#ff`).

### Typed literals

A type prefix forces the literal's type, separated from the
value by `#`:

| Form | Example | Type |
|------|---------|------|
| `BYTE#<int>` | `BYTE#1` | `BYTE` (8-bit unsigned) |
| `WORD#<int>` | `WORD#16#FFFF` | `WORD` (16-bit unsigned) |
| `DWORD#<int>` | `DWORD#16#DEAD_BEEF` | `DWORD` (32-bit unsigned) |
| `LWORD#<int>` | `LWORD#0` | `LWORD` (64-bit unsigned) |
| `SINT#<int>` | `SINT#-1` | `SINT` (8-bit signed) |
| `INT#<int>` | `INT#-3` | `INT` (16-bit signed) |
| `DINT#<int>` | `DINT#100000` | `DINT` (32-bit signed) |
| `LINT#<int>` | `LINT#0` | `LINT` (64-bit signed) |
| `UINT#<int>` | `UINT#42` | `UINT` (16-bit unsigned) |
| `UDINT#<int>` | `UDINT#0` | `UDINT` (32-bit unsigned) |
| `ULINT#<int>` | `ULINT#0` | `ULINT` (64-bit unsigned) |

A typed literal can combine with any base:
`BYTE#16#FF`, `INT#2#1010`, `DWORD#8#777`.

## Syntax

```text
integer_literal :=
      decimal_literal
    | "2#" binary_digits
    | "8#" octal_digits
    | "16#" hex_digits
    | type_name "#" integer_literal

decimal_literal := ['+' | '-'] decimal_digit { ['_'] decimal_digit }
```

### Examples

```iec-st
iCount   : INT  := 42;            (* untyped, widens to INT *)
bMask    : BYTE := 16#FF;         (* hex literal → BYTE 255 *)
iSigned  : INT  := INT#-3;        (* typed literal *)
dwFlags  : DWORD := DWORD#16#DEAD_BEEF;
bPattern : BYTE := 2#1010_1100;   (* binary, underscore for readability *)
```

## Semantics

An untyped integer literal has the type of the smallest
standard integer type that can hold it, with promotion to match
its surrounding expression. A typed literal always has exactly
the type of its prefix; passing a typed literal to a parameter
of a different type triggers an explicit-conversion error
unless an implicit widening rule applies.

## IEC reference

IEC 61131-3 third edition (2013), clause **6.3.1** — "Numeric
literals". Underscore-as-digit-separator is in 6.3.1 paragraph 3.

## matiec conformance

matiec accepts all four bases and all typed-literal prefixes
listed above. **Two emit-bugs** are documented in the
`llm_signals` block above and are worth repeating here:

1. **Hex literal in CASE label** (`16#01:` etc.) → lexer
   tokenises `16#` as a type prefix and chokes on the bare
   `01`. Workaround: decimal labels.
2. **Typed literal as function argument** (`SHL(BYTE#1, x)`)
   → matiec emits `data__->BYTE` instead of an integer
   constant, failing g++ on the PLC. Workaround: pre-compute
   the value, or use an explicit conversion call
   (`INT_TO_BYTE(1)`).

Both quirks were observed and worked around in the
Ackersteuerung-2026-05-14 cleanup; they are reproducible with
the matiec version shipped in ForgeIEC at the time of writing.
A future matiec++/rustly backend (see Memory:
`project_codegen_cxx_migration` /
`project_rusty_evaluation`) is expected to make these
quirks go away.

## ForgeIEC notes

The ForgeIEC editor's tree-sitter highlighter recognises all
prefixes in this table and colours them as constants. The
auto-completion suggests `INT_TO_BYTE` and `BYTE_TO_INT` when
it detects an obvious type-mismatch in a literal context.

When defining initial values via `project.write.add_variable`,
prefer untyped literals (`1`, `2`, `42`) for primitive types —
the editor's pool computes the IEC type from the variable's
declared type, and an untyped literal will match without a
prefix.
