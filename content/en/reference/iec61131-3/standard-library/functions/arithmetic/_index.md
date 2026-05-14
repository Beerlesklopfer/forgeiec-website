---
title: "Arithmetic functions"
summary: "ABS, SQRT, LN, LOG, EXP plus the trig family SIN/COS/TAN and inverse trig ASIN/ACOS/ATAN. Operate on REAL/LREAL by default; ABS also on integers."
weight: 20
iec_chapter: "Annex F.2.2"
construct_kind: "function"
keywords: ["ABS", "SQRT", "LN", "LOG", "EXP", "SIN", "COS", "TAN", "ASIN", "ACOS", "ATAN"]
llm_signals:
  - error_pattern: "ABS expected ANY_NUM"
    where: "matiec"
    diagnosis: "ABS only takes signed numeric types. Calling it on UINT/UDINT/UBYTE (already non-negative) is a type error."
    fix_strategy: "Drop the ABS call on unsigned types — they're already non-negative by definition."
    fix_example: |
      (* before — fails *)
      iResult := ABS(uIndex);
      (* after — UINT is already >= 0 *)
      iResult := UINT_TO_INT(uIndex);
  - error_pattern: "SQRT of negative"
    where: "runtime"
    diagnosis: "SQRT of a negative REAL produces NaN per IEEE-754. matiec doesn't trap; the result silently propagates as NaN through subsequent calculations."
    fix_strategy: "Range-check before calling SQRT. If a negative is possible, decide whether to clip to 0, return an error code, or use ABS first."
    fix_example: |
      IF rValue >= 0.0 THEN
          rResult := SQRT(rValue);
      ELSE
          rResult := 0.0;
      END_IF;
  - error_pattern: "LN of zero or negative"
    where: "runtime"
    diagnosis: "LN(0) is -Infinity, LN(<0) is NaN per IEEE-754. Same warning as SQRT — silent propagation."
    fix_strategy: "Range-check the input. For values that legitimately approach zero, add a small epsilon: `LN(rValue + 1.0e-9)`."
---

## ABS — absolute value

`ABS(IN: ANY_NUM): ANY_NUM` — same type out as in. Returns
`|IN|`. Operates on signed integers (`SINT`, `INT`, `DINT`,
`LINT`) and on `REAL` / `LREAL`. **Does NOT take unsigned
types** — they're already non-negative.

```iec-st
iAbs := ABS(-3);          (* → 3 *)
rAbs := ABS(-2.5);        (* → 2.5 *)
diMag := ABS(diSigned);
```

## SQRT, LN, LOG, EXP

| Function | Signature | Notes |
|---|---|---|
| `SQRT` | `(REAL): REAL` | Square root. Negative input → NaN |
| `LN` | `(REAL): REAL` | Natural log (base e). 0 → -∞, <0 → NaN |
| `LOG` | `(REAL): REAL` | Common log (base 10). Same caveats |
| `EXP` | `(REAL): REAL` | `e^IN`. Overflow at ~88 → +∞ |

```iec-st
rRoot := SQRT(2.0);            (* → 1.4142… *)
rNatLog := LN(2.71828);        (* → ~1.0 *)
rLog10  := LOG(100.0);         (* → 2.0 *)
rExp    := EXP(1.0);           (* → e ≈ 2.71828 *)
```

`LREAL` versions exist when more precision is needed:
`SQRT_LREAL`, `LN_LREAL`, etc. — naming is implementation-
specific in matiec, look up via `library.read_block`.

## Trigonometric: SIN, COS, TAN

`SIN(REAL): REAL` etc. **All angles in radians.** If you have
degrees, convert with `rRad := rDeg * 3.14159 / 180.0;`.

```iec-st
rSin := SIN(0.0);              (* → 0.0 *)
rCos := COS(3.14159);          (* → -1.0 *)
rTan := TAN(0.7854);           (* → ~1.0 (π/4) *)
```

`TAN` of `(π/2 + n·π)` is mathematically infinite; in IEEE-754
it's a very large finite number (not `±∞`).

## Inverse trig: ASIN, ACOS, ATAN

`ASIN(REAL): REAL` returns angle in radians; domain `[-1.0, 1.0]`.
`ACOS(REAL): REAL` returns angle in radians; domain `[-1.0, 1.0]`.
`ATAN(REAL): REAL` returns angle in radians; domain unrestricted.

Out-of-domain `ASIN`/`ACOS` returns NaN — same caveat as SQRT.

For two-argument arc-tangent (`atan2`-style, returns full
quadrant), the IEC standard library has no `ATAN2`. matiec
exposes a non-standard extension via `ATAN2_REAL`; portability-
critical code should compute the quadrant by hand from `SIN`
and `COS`.

## Type families

The standard treats most of these as `(ANY_REAL): ANY_REAL`
generic — matiec accepts both `REAL` and `LREAL` and returns
the matching type. Mixing `REAL` and `LREAL` in one expression
needs `REAL_TO_LREAL` or `LREAL_TO_REAL` ([type-conversion](../type-conversion/)).

## IEC reference

IEC 61131-3 third edition (2013), Annex **F.2.2** —
"Numerical functions" Tables F.4–F.6.

## matiec conformance

matiec implements all standard arithmetic functions per the
spec. Trig precision is the underlying C library's
(`libm`) precision — typically a few ULP for normal inputs.

The `LREAL`-suffixed versions (`SIN_LREAL`, `SQRT_LREAL`, …)
are matiec's way to disambiguate when the standard's
generic `(ANY_REAL): ANY_REAL` typing isn't enough.
