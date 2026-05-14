---
title: "Comparison operators"
summary: "=, <>, <, <=, >, >= — return BOOL. Operands must share the same IEC type, no implicit promotion."
weight: 30
iec_chapter: "6.6.1"
construct_kind: "operator"
keywords: ["=", "<>", "<", "<=", ">", ">=", "comparison"]
llm_signals:
  - error_pattern: "comparison of integer expressions of different types"
    where: "matiec"
    diagnosis: "The two operands of `=`/`<>`/`<`/`>`/`<=`/`>=` have different IEC types — typically INT vs UINT, BYTE vs INT, or DINT vs INT. matiec's strict typing rejects the comparison."
    fix_strategy: "Convert one operand explicitly to match the other's type. Pick the wider / signed type as the target so values from both sides fit (`UINT_TO_INT` is safe for the lower half; `INT_TO_DINT` is always safe)."
    fix_example: |
      (* before — fails *)
      IF iStep = uIndex THEN ... END_IF;        (* INT vs UINT *)
      (* after — promote UINT to INT *)
      IF iStep = UINT_TO_INT(uIndex) THEN ... END_IF;
  - error_pattern: "comparison of REAL with ="
    where: "(any)"
    diagnosis: "Direct equality comparison of REAL or LREAL values is unsafe due to floating-point precision (`0.1 + 0.2 = 0.3` is FALSE in IEEE-754). Not a matiec error per se but a runtime correctness issue."
    fix_strategy: "Compare with a tolerance: `ABS(rA - rB) < epsilon` instead of `rA = rB`. Pick epsilon based on the magnitude of the values being compared."
    fix_example: |
      (* before — flaky at runtime *)
      IF rTemperature = 25.0 THEN ... END_IF;
      (* after — robust *)
      IF ABS(rTemperature - 25.0) < 0.01 THEN ... END_IF;
---

## Operators

| Operator | Meaning | Operand types | Result |
|---|---|---|---|
| `=` | Equal | `ANY_NUM`, `BOOL`, `STRING`, `TIME`, … (any) — both same | `BOOL` |
| `<>` | Not equal | as above | `BOOL` |
| `<` | Less than | `ANY_NUM`, `STRING`, `TIME`, `DATE`, `TOD` | `BOOL` |
| `<=` | Less than or equal | as above | `BOOL` |
| `>` | Greater than | as above | `BOOL` |
| `>=` | Greater than or equal | as above | `BOOL` |

`=` and `<>` work on every comparable type; `<`/`<=`/`>`/`>=`
require an ordering, so they're undefined on `BOOL` and on
custom enumerated types without an ordering hint.

## Type-matching rule

Both operands must share the same IEC type. matiec rejects
implicit promotion (see `llm_signals`). Always wrap one side
in the explicit conversion:

```iec-st
(* INT vs UINT — fails *)
(* IF iA = uB THEN ... END_IF; *)

(* INT vs UINT — works after promotion *)
IF iA = UINT_TO_INT(uB) THEN ... END_IF;

(* INT vs DINT — promote INT to DINT *)
IF INT_TO_DINT(iA) >= dwBig THEN ... END_IF;
```

## REAL comparison hazard

`REAL` and `LREAL` are IEEE-754 floats. Direct equality is
flaky:

```iec-st
(* Don't do this *)
IF rValue = 0.1 + 0.2 THEN ... END_IF;     (* FALSE in IEEE-754 *)

(* Do this *)
IF ABS(rValue - 0.3) < 0.0001 THEN ... END_IF;
```

For comparisons that should treat "equal within tolerance" as
equal, use `ABS(a - b) < epsilon`. Pick epsilon based on the
magnitude of the values: a temperature in degrees Celsius can
tolerate `0.01`; a normalised position in `[0..1]` should use
something smaller.

## STRING comparison

String operators compare lexicographically by character
ordinal. `'apple' < 'banana'` is `TRUE`. Comparison is
case-sensitive — `'Apple' = 'apple'` is `FALSE`. For
case-insensitive comparison, normalise both sides first
(IEC has no built-in `tolower`; use a per-project FUN).

## IEC reference

IEC 61131-3 third edition (2013), clause **6.6.1** Table 55.

## matiec conformance

matiec implements all six comparison operators correctly. The
type-strictness rule is enforced more aggressively than some
other dialects (Codesys, B&R Automation Studio) — code
ported from those tools often needs explicit conversions
inserted at every comparison site.
