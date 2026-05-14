---
title: "Arithmetic operators"
summary: "+, -, *, /, MOD, **. Operate on ANY_NUM types; both operands must share a type — no implicit promotion."
weight: 10
iec_chapter: "6.6.1"
construct_kind: "operator"
keywords: ["+", "-", "*", "/", "MOD", "**", "arithmetic"]
llm_signals:
  - error_pattern: "binary operator '\\+' applied to incompatible types"
    where: "matiec"
    diagnosis: "Two operands of different IEC numeric types — typically `INT + UINT`, `DINT + INT`, `INT + REAL`. matiec does not auto-promote."
    fix_strategy: "Convert one side explicitly to match the other. Pick the wider / more permissive type as the target: `INT_TO_DINT`, `INT_TO_REAL`, `UINT_TO_INT`, etc."
    fix_example: |
      (* before — fails *)
      result := iCount + udCount;        (* INT + UDINT *)
      (* after — promote INT to UDINT *)
      result := INT_TO_UDINT(iCount) + udCount;
  - error_pattern: "division by zero"
    where: "runtime"
    diagnosis: "Integer division by zero is a runtime fault on most PLCs (the runtime usually halts the task or raises an exception). REAL division by zero produces ±Infinity or NaN per IEEE-754."
    fix_strategy: "Guard the divisor with an `IF` before dividing, or use a clamping pattern: `result := numerator / SEL(divisor = 0, divisor, 1)`."
    fix_example: |
      (* before — runtime fault when divisor=0 *)
      rRatio := rNum / rDenom;
      (* after — guarded *)
      IF rDenom <> 0.0 THEN
          rRatio := rNum / rDenom;
      ELSE
          rRatio := 0.0;
      END_IF;
  - error_pattern: "MOD applied to REAL"
    where: "matiec"
    diagnosis: "`MOD` is integer-only in IEC 61131-3. Floating-point modulo is not provided."
    fix_strategy: "Convert REAL to DINT for integer remainder, or implement the float remainder by hand: `rRem := rA - TRUNC(rA / rB) * rB`."
    fix_example: |
      (* before — fails *)
      rRem := rA MOD rB;
      (* after — float remainder via TRUNC *)
      rRem := rA - TRUNC(rA / rB) * rB;
---

## Operators

| Operator | Operand types | Result | Notes |
|---|---|---|---|
| `+` | `ANY_NUM`, both same type | same type | Addition |
| `-` (binary) | `ANY_NUM` | same | Subtraction |
| `-` (unary) | `ANY_NUM` (signed) | same | Negation. Unsigned types reject unary minus |
| `*` | `ANY_NUM` | same | Multiplication |
| `/` | `ANY_NUM` | same | Division (integer truncates toward zero) |
| `MOD` | `ANY_INT` | same | Integer remainder. Sign follows dividend |
| `**` | `ANY_REAL`, exponent `ANY_NUM` | `ANY_REAL` | Exponentiation. Right-associative |

`ANY_NUM` covers the integer types (`SINT`/`INT`/`DINT`/`LINT`
and unsigned variants) and the real types (`REAL`/`LREAL`).
`ANY_INT` is the integer subset only.

## Type-matching rule

Both operands of a binary arithmetic operator must have the
**same** IEC type. matiec does not promote `INT` to `DINT`
or `INT` to `REAL` automatically. Use the explicit conversion
functions when types differ:

```iec-st
(* INT + DINT — needs explicit promotion *)
dwSum := INT_TO_DINT(iCount) + dwBig;

(* INT * REAL — needs INT_TO_REAL or REAL division of INT *)
rArea := INT_TO_REAL(iWidth) * INT_TO_REAL(iHeight);

(* unary minus on UINT — illegal *)
(* iN := -uVal;  (* fails *) *)
iN := -UINT_TO_INT(uVal);
```

## Integer overflow

Integer arithmetic does **not** trap on overflow. `SINT#127 + 1`
silently wraps to `SINT#-128`. If overflow detection matters,
either use a wider type for the calculation:

```iec-st
diSum := SINT_TO_DINT(iA) + SINT_TO_DINT(iB);
IF diSum > 127 OR diSum < -128 THEN ... END_IF;
```

…or guard against the operands ahead of time.

## REAL precision

`REAL` is IEEE-754 single precision (~7 decimal digits).
`LREAL` is IEEE-754 double (~15 digits). Comparing `REAL`
values with `=` is unsafe — always use a tolerance:

```iec-st
IF ABS(rA - rB) < 0.0001 THEN ... END_IF;
```

## IEC reference

IEC 61131-3 third edition (2013), clause **6.6.1** Table 55 —
"Operators of the ST language".

## matiec conformance

matiec implements the standard arithmetic operators correctly.
The two main pitfalls are documented in `llm_signals` above:

- Strict type-matching (no implicit promotion).
- `MOD` is integer-only.

There is **no `**` emit-bug** but performance of `**` on a PLC
is poor (it lowers to a `pow()` call). Prefer `x * x * x`
over `x ** 3` for small constant exponents in scan-cycle code.
