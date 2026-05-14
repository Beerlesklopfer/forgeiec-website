---
title: "Standard Library"
summary: "Built-in functions and function blocks defined by IEC 61131-3."
weight: 60
---

## Standard Library

Functions and function blocks that every IEC 61131-3
implementation must ship.

### [Functions](functions/)

Pure functions — no instance, called directly.

- [Type-conversion](functions/type-conversion/) — `<SRC>_TO_<DST>`,
  `TRUNC`, BCD codecs.
- [Arithmetic](functions/arithmetic/) — `ABS`, `SQRT`,
  `LN`/`LOG`/`EXP`, trig + inverse trig.
- [Comparison functions](functions/comparison-functions/) — `GT`,
  `GE`, `EQ`, `LE`, `LT`, `NE` (the function-form of the
  comparison operators; useful for variadic chained checks).
- [Selection](functions/selection/) — `SEL`, `MUX`, `MIN`,
  `MAX`, `LIMIT`.
- [String](functions/string/) — `LEN`, `LEFT`/`RIGHT`/`MID`,
  `CONCAT`, `INSERT`, `DELETE`, `REPLACE`, `FIND`.
- [Bit](functions/bit/) — `SHL`, `SHR`, `ROL`, `ROR`. **Includes
  the matiec emit-bug warning for `SHL(BYTE#1, …)`.**

### [Function blocks](function-blocks/)

Stateful — declare an instance, then call the instance.

- Bistables: [`SR`](function-blocks/sr/) (set-dominant),
  [`RS`](function-blocks/rs/) (reset-dominant).
- Edge detectors: [`R_TRIG`](function-blocks/r-trig/) (rising),
  [`F_TRIG`](function-blocks/f-trig/) (falling).
- Counters: [`CTU`](function-blocks/ctu/),
  [`CTD`](function-blocks/ctd/), [`CTUD`](function-blocks/ctud/).
- Timers: [`TON`](function-blocks/ton/),
  [`TOF`](function-blocks/tof/), [`TP`](function-blocks/tp/).
- Communication FBs (IEC 61131-5). (Not in matiec; project-
  specific extensions in ForgeIEC.)
