---
title: "Elementary data types"
summary: "BOOL, the integer family (signed + unsigned, 8/16/32/64 bit), the bit-string family, REAL/LREAL, the time/date family, and STRING."
weight: 10
iec_chapter: "6.4.1"
construct_kind: "type"
keywords: ["BOOL", "INT", "BYTE", "REAL", "TIME", "STRING", "DATE", "TOD"]
llm_signals:
  - error_pattern: "type 'TIME' expected"
    where: "matiec"
    diagnosis: "A FB or function input declared as `TIME` is being given an integer literal. Common with TON's PT pin: `tonStep(IN := x, PT := 100)` instead of `T#100ms`."
    fix_strategy: "Use a TIME literal: `T#100ms`, `T#1s`, `T#1m30s`, `T#1d12h`. Or declare a `tStep : TIME := T#100ms;` and pass that."
    fix_example: |
      (* before — fails *)
      tonStep(IN := xStart, PT := 100);
      (* after *)
      tonStep(IN := xStart, PT := T#100ms);
  - error_pattern: "INT range exceeded"
    where: "matiec"
    diagnosis: "An integer literal exceeds the declared variable's type range. E.g. `iVal : INT := 100000;` (INT max is 32 767)."
    fix_strategy: "Either widen the variable type (`INT` → `DINT`) or pick a value in range. Don't silently truncate."
    fix_example: |
      (* before *)
      iVal : INT := 100000;
      (* after — option A: widen *)
      iVal : DINT := 100000;
      (* after — option B: in range *)
      iVal : INT := 32000;
  - error_pattern: "STRING length cannot be negative"
    where: "FStCompiler"
    diagnosis: "STRING type declared with a non-positive length: `STRING(0)` or `STRING(-1)`."
    fix_strategy: "STRING length must be a positive integer literal. Default (omitted) is implementation-defined — typically 80 chars on matiec."
    fix_example: |
      (* before — fails *)
      sName : STRING(0);
      (* after *)
      sName : STRING(80);   (* explicit 80-char *)
      sShort : STRING(16);  (* shorter when the use-case allows *)
---

## BOOL

Single bit, two values: `TRUE` and `FALSE`.

- Default initial value is `FALSE`.
- Truthy coercion does NOT exist — `IF iCount THEN ...` is a
  type error. Always compare explicitly: `IF iCount > 0 THEN`.
- BOOL operands work with `AND` / `OR` / `XOR` / `NOT` as
  logical operators; the same operators on `BYTE`/`WORD`/`DWORD`
  are bitwise.

## Integer family

Signed integers in four widths plus their unsigned cousins:

| Type | Width | Range |
|---|---|---|
| `SINT` | 8-bit signed | -128..127 |
| `INT` | 16-bit signed | -32 768..32 767 |
| `DINT` | 32-bit signed | ±2¹⁰⁹ ... wait, ±2³¹ |
| `LINT` | 64-bit signed | ±2⁶³ |
| `USINT` | 8-bit unsigned | 0..255 |
| `UINT` | 16-bit unsigned | 0..65 535 |
| `UDINT` | 32-bit unsigned | 0..2³²-1 |
| `ULINT` | 64-bit unsigned | 0..2⁶⁴-1 |

Default initial value: `0`.

Arithmetic does **not trap on overflow** — `SINT#127 + 1`
silently wraps to `-128`. If overflow detection matters, use
the next-wider type for the calculation.

Conversions between integer types are explicit:
`INT_TO_DINT`, `DINT_TO_INT`, `INT_TO_UINT`, `UINT_TO_INT`,
`SINT_TO_INT`, `INT_TO_SINT`, etc.

## Bit-string family

Same widths as the unsigned integers but used for bit-pattern
operations rather than arithmetic:

| Type | Width |
|---|---|
| `BYTE` | 8 bits |
| `WORD` | 16 bits |
| `DWORD` | 32 bits |
| `LWORD` | 64 bits |

Bit-string operands work with `AND` / `OR` / `XOR` / `NOT`
bitwise (in contrast with BOOL operands, which are logical).
Bit access via `.N` syntax: `bMask.0`, `wReg.15`.

Default initial value: `0`.

Conversions: `BYTE_TO_INT`, `INT_TO_BYTE`, `WORD_TO_DWORD`,
etc. Conversion to BOOL via `<> 0` test.

## REAL family

IEEE-754 floating point:

| Type | Width | Significant digits |
|---|---|---|
| `REAL` | 32 bits | ~7 |
| `LREAL` | 64 bits | ~15 |

Default initial value: `0.0`.

**Comparison hazard**: `REAL` equality is unsafe due to
floating-point precision. Use `ABS(rA - rB) < epsilon`
instead of `rA = rB`. See
[comparison operators](../../textual/structured-text/operators/comparison/).

## Time, date and time-of-day

| Type | Literal example | Meaning |
|---|---|---|
| `TIME` | `T#1h30m`, `T#100ms` | Duration |
| `DATE` | `D#2026-05-14` | Calendar date |
| `TIME_OF_DAY` / `TOD` | `TOD#14:30:00` | Wall-clock time |
| `DATE_AND_TIME` / `DT` | `DT#2026-05-14-14:30:00` | Combined timestamp |

`TIME` is the most common — it's the type of TON's `PT` input
and `ET` output. Write durations with the `T#` prefix:

```iec-st
T#100ms     (* 100 milliseconds *)
T#1s        (* 1 second *)
T#1m30s     (* 1 minute 30 seconds *)
T#1h        (* 1 hour *)
T#1d12h     (* 1.5 days *)
T#-500ms    (* negative duration: 500 ms in the past *)
```

Default initial value: `T#0s`, `D#1970-01-01`,
`TOD#00:00:00`, `DT#1970-01-01-00:00:00`.

## STRING

Variable-length character string with a declared maximum
length:

```iec-st
sName : STRING(80);                 (* 80 chars max *)
sLine : STRING(255) := 'hello';    (* with initial value *)
sShort : STRING;                    (* default length, 80 on matiec *)
```

String literals use **single** quotes: `'hello'`. Embedded
single-quote: `'$''`. Escape sequences with `$` prefix:
`$N` (newline), `$T` (tab), `$$` (literal $).

Default initial value: empty string `''`.

## IEC reference

IEC 61131-3 third edition (2013), clause **6.4.1** —
"Elementary data types" Table 10.

## matiec conformance

matiec implements all elementary types per the standard. The
three pitfalls in `llm_signals` are the recurring LLM trap
points:

- TIME literals require `T#` prefix.
- Integer-literal range vs. declared type.
- STRING(N) needs N > 0.

## ForgeIEC notes

The pool stores the IEC type as a string. When you call
`project.write.add_variable iecType="INT"`, the variable is
created with type `INT` exactly; no remapping happens.
