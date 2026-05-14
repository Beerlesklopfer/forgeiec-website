---
title: "Standard functions"
summary: "Built-in pure functions of IEC 61131-3 — type-conversion, arithmetic, comparison, selection, string and bit operations."
weight: 10
---

## Standard functions

The Function (FUN) entries defined by the IEC 61131-3 standard.
All are pure: same input → same output, no internal state.
Called directly with positional or named parameters; **no
instance declaration needed** (unlike Function Blocks).

### Sub-pages

- [Type-conversion](type-conversion/) — `<SRC>_TO_<DST>`,
  `TRUNC`, `BCD_TO_INT`, `INT_TO_BCD`. The single most-called
  family in matiec-strict code.
- [Arithmetic](arithmetic/) — `ABS`, `SQRT`, `LN`, `LOG`,
  `EXP`, `SIN`, `COS`, `TAN`, `ASIN`, `ACOS`, `ATAN`.
- [Comparison functions](comparison-functions/) — `GT`, `GE`,
  `EQ`, `LE`, `LT`, `NE`. Variadic versions of the comparison
  operators for IL.
- [Selection](selection/) — `SEL`, `MUX`, `MIN`, `MAX`,
  `LIMIT`. Conditional value-picking without an IF.
- [String](string/) — `LEN`, `LEFT`, `RIGHT`, `MID`, `CONCAT`,
  `INSERT`, `DELETE`, `REPLACE`, `FIND`.
- [Bit](bit/) — `SHL`, `SHR`, `ROL`, `ROR`. **Includes the
  matiec emit-bug warning for `SHL(BYTE#1, …)`.**

Each sub-page consolidates the whole family in one document
(no per-function pages). Use the page-internal table of
contents to jump to a specific function.
