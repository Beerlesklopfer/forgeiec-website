---
title: "Operators"
summary: "Arithmetic, bitwise, comparison, logical and assignment operators with precedence + operand-type rules."
weight: 20
iec_chapter: "6.6.1"
construct_kind: "operator"
---

## Operators

Structured Text expressions are built from operators acting on
typed operands. The same operator symbol can apply to multiple
types (`+` for `INT` and for `REAL`), but operand types must
match exactly — there is no implicit promotion across families.

### Sub-pages

- [Arithmetic](arithmetic/) — `+`, `-`, `*`, `/`, `MOD`, `**`.
- [Bitwise](bitwise/) — `AND`, `OR`, `XOR`, `NOT`. Note these
  same keywords are also the **logical** operators when applied
  to `BOOL`; the distinction is operand-type.
- [Comparison](comparison/) — `=`, `<>`, `<`, `<=`, `>`, `>=`.
- [Assignment + precedence](assignment-and-precedence/) — `:=`
  and the full operator-precedence table (highest to lowest).

## Quick reference: precedence table

From highest to lowest binding strength. Operators of the same
precedence associate left-to-right (except `**` which is
right-associative).

| Class | Operators | Notes |
|---|---|---|
| Parentheses | `(...)` | Highest — overrides everything |
| Function call | `name(...)` | Includes FB instance call |
| Exponent | `**` | Right-associative |
| Unary | `-` (negation), `NOT` | Unary minus, logical/bitwise NOT |
| Multiplicative | `*`, `/`, `MOD` | |
| Additive | `+`, `-` | |
| Comparison | `<`, `<=`, `>`, `>=` | |
| Equality | `=`, `<>` | |
| Bitwise/Logical AND | `AND`, `&` | `&` and `AND` synonymous |
| Bitwise/Logical XOR | `XOR` | |
| Bitwise/Logical OR | `OR` | Lowest binding strength |

`AND` / `OR` / `XOR` / `NOT` are simultaneously **logical**
(when both operands are `BOOL`) and **bitwise** (when both are
`BYTE` / `WORD` / `DWORD` / `LWORD`). Mixing a `BOOL` and a
`BYTE` is a type error — use `BOOL_TO_BYTE` / `BYTE_TO_BOOL`
to convert explicitly.

## IEC reference

IEC 61131-3 third edition (2013), clause **6.6.1** —
"Operators of the ST language".

## ForgeIEC notes

The editor's tree-sitter highlighter colours the operator
keywords distinctly from other identifiers. Auto-completion
will not suggest type-incompatible operands.
