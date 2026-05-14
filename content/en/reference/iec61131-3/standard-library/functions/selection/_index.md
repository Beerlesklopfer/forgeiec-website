---
title: "Selection functions"
summary: "SEL, MUX, MIN, MAX, LIMIT — pick a value without writing IF."
weight: 30
iec_chapter: "Annex F.2.4"
construct_kind: "function"
keywords: ["SEL", "MUX", "MIN", "MAX", "LIMIT"]
llm_signals:
  - error_pattern: "MIN/MAX expected ANY_NUM"
    where: "matiec"
    diagnosis: "MIN/MAX work on numeric and STRING types but not on BOOL or BYTE-as-bit-string. Calling them on BOOL is a type error."
    fix_strategy: "Use OR (BOOL MAX) / AND (BOOL MIN) instead — they're the boolean equivalents."
    fix_example: |
      (* before — fails *)
      xAny := MAX(xA, xB);
      (* after *)
      xAny := xA OR xB;
  - error_pattern: "LIMIT bounds out of order"
    where: "runtime"
    diagnosis: "If `MN > MX` then LIMIT's behaviour is undefined per the standard. matiec returns IN unchanged in this case (silent)."
    fix_strategy: "Validate that MN <= MX before calling LIMIT, or compute the bounds in a way that guarantees ordering."
---

## SEL — binary select

`SEL(G: BOOL, IN0: ANY, IN1: ANY): ANY` — returns `IN0` when
`G = FALSE`, `IN1` when `G = TRUE`. Both `IN0` and `IN1` must
be the same type; the result has that type.

```iec-st
iResult := SEL(xMode, iValueA, iValueB);
(* iResult := iValueA when xMode is FALSE
   iResult := iValueB when xMode is TRUE *)
```

Equivalent to:
```iec-st
IF xMode THEN iResult := iValueB; ELSE iResult := iValueA; END_IF;
```

## MUX — multi-way select

`MUX(K: ANY_INT, IN0: ANY, IN1: ANY, IN2: ANY, ...): ANY` —
returns `IN<K>`. The number of `IN` arguments is variable and
must cover the range of `K`. Out-of-range `K` is implementation-
defined (matiec returns `IN0`).

```iec-st
iResult := MUX(iSelector, 10, 20, 30, 40);
(* iResult := 10 when iSelector=0, 20 when 1, etc. *)
```

`MUX` is essentially a poor-man's `CASE`-as-expression — useful
when you need to compute one of N values inside a larger
expression where `CASE` (a statement) wouldn't fit.

## MIN, MAX — extremum of variadic args

`MIN(IN1: ANY_NUM, IN2: ANY_NUM, ...): ANY_NUM` — smallest of
all inputs. All arguments must share a type.

`MAX(IN1: ANY_NUM, IN2: ANY_NUM, ...): ANY_NUM` — largest.

```iec-st
iSmallest := MIN(iA, iB, iC, iD);
rPeak     := MAX(rSensor1, rSensor2, rSensor3);
```

For BOOLs, use `AND` (boolean MIN: TRUE if ALL are TRUE) and
`OR` (boolean MAX: TRUE if ANY is TRUE) — see `llm_signals`.

## LIMIT — clamp to a range

`LIMIT(MN: ANY_NUM, IN: ANY_NUM, MX: ANY_NUM): ANY_NUM` —
returns `IN` clamped to `[MN, MX]`:

```text
result := MAX(MN, MIN(IN, MX))
```

```iec-st
(* clamp a sensor reading to the valid PT100 range *)
rTemperature := LIMIT(MN := -50.0,
                      IN := rRawTemp,
                      MX := 200.0);

(* clamp an INT step counter *)
iStep := LIMIT(0, iStepRaw, 5);
```

LIMIT is the standard idiom for "saturate at boundaries" —
prefer it over hand-written `IF` cascades when the bounds are
known.

## IEC reference

IEC 61131-3 third edition (2013), Annex **F.2.4** —
"Selection functions" Table F.8.

## matiec conformance

All five functions implemented per the standard. The variadic
forms (`MUX`, `MIN`, `MAX` with N inputs) accept up to 32
inputs in matiec — the standard doesn't bound this.

LIMIT's behaviour when `MN > MX` is undefined per the spec;
matiec returns `IN` unchanged. Validate the bounds yourself
when they're computed at runtime.
