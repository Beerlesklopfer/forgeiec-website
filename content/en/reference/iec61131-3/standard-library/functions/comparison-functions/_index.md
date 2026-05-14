---
title: "Comparison functions"
summary: "GT, GE, EQ, LE, LT, NE — function-form versions of the comparison operators. Useful in IL and as variadic chained checks in ST."
weight: 60
iec_chapter: "Annex F.2.4"
construct_kind: "function"
keywords: ["GT", "GE", "EQ", "LE", "LT", "NE", "comparison"]
---

## GT, GE, EQ, LE, LT, NE

The IEC standard provides function-form comparison operators
in addition to the infix `<`, `<=`, `=`, `>=`, `>`, `<>`:

| Function | Equivalent | Meaning |
|---|---|---|
| `GT(IN1, IN2): BOOL` | `IN1 > IN2` | Greater than |
| `GE(IN1, IN2): BOOL` | `IN1 >= IN2` | Greater than or equal |
| `EQ(IN1, IN2): BOOL` | `IN1 = IN2` | Equal |
| `LE(IN1, IN2): BOOL` | `IN1 <= IN2` | Less than or equal |
| `LT(IN1, IN2): BOOL` | `IN1 < IN2` | Less than |
| `NE(IN1, IN2): BOOL` | `IN1 <> IN2` | Not equal |

In Structured Text these are equivalent to the infix
operators and most projects use `>`, `<`, `=` directly. The
function form has two genuine use cases:

1. **In IL** (Instruction List), where the accumulator-style
   syntax doesn't have infix operators.
2. **In variadic chained checks** in ST — see below.

## Variadic chained form

`GT(IN1, IN2, IN3, ...)` returns `TRUE` only when the values
are **strictly decreasing** in order. Equivalent to
`(IN1 > IN2) AND (IN2 > IN3) AND ...`.

The same pattern applies to `GE`, `LE`, `LT` (chain in the
matching direction). `EQ`, `NE` chain pairwise:
`EQ(IN1, IN2, IN3) := (IN1 = IN2) AND (IN2 = IN3)`.

```iec-st
(* "is x in (5, 10) exclusive?" — chained GT *)
xInRange := GT(10, iX, 5);

(* monotone-decreasing series check *)
xMonotonic := GT(iA, iB, iC, iD);
```

These chained forms read more cleanly than the equivalent
infix-AND chain when the relation is the same throughout.

## Type-matching rule

Same as the infix operators: all arguments must share a type.
matiec is strict — see
[textual/structured-text/operators/comparison](../../../textual/structured-text/operators/comparison/).

## IEC reference

IEC 61131-3 third edition (2013), Annex **F.2.4** —
"Comparison functions" Table F.9.

## matiec conformance

All six functions implemented per the standard, including the
variadic chained form.
