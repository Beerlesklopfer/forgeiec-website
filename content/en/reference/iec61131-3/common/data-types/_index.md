---
title: "Data types"
summary: "Elementary, generic and derived IEC 61131-3 data types. Foundation for every variable declaration."
weight: 20
iec_chapter: "6.4"
construct_kind: "type"
---

## Data types

Every IEC 61131-3 variable has a **type**. The type controls
storage size, value range, allowed operations, and which
conversion calls are needed when the value is used somewhere
expecting a different type.

### Sub-pages

- [Elementary types](elementary-types/) — `BOOL`, `BYTE`,
  `INT`, `REAL`, `TIME`, `STRING` and their cousins. The
  building blocks.
- Generic types `ANY`, `ANY_NUM`, `ANY_INT`, `ANY_BIT`, `ANY_REAL`
  appear in standard-library function signatures (e.g.
  `ABS(IN: ANY_NUM): ANY_NUM`). They cannot be used in user
  variable declarations. (Stub.)
- Derived types — `STRUCT`, `ARRAY`, enumerations, type-safe
  aliases (`TYPE … : … END_TYPE`). (Stub.)

## Type-strict philosophy

IEC 61131-3 is strongly typed and matiec is among the
strictest implementations. Two key consequences:

1. **No implicit conversion across families.** `INT + REAL` is
   a type error; you write `INT_TO_REAL(i) + r`. `INT vs UINT`
   is a comparison error; you write `i = UINT_TO_INT(u)`.
2. **No "truthy" coercion.** `IF iCount THEN …` is illegal —
   the condition must be an explicit BOOL: `IF iCount > 0 THEN`.

These rules trade convenience at the call site for
predictability at run-time. PLC code outlives its writer
and runs unattended; the type-strictness pays back when the
next maintainer reads the code.

## Quick reference: type widths

| Type | Width | Range / values |
|---|---|---|
| `BOOL` | 1 bit | `FALSE`, `TRUE` |
| `BYTE` | 8 bits | bit string, 0..255 unsigned |
| `WORD` | 16 bits | bit string, 0..65535 unsigned |
| `DWORD` | 32 bits | bit string, 0..2³²-1 unsigned |
| `LWORD` | 64 bits | bit string, 0..2⁶⁴-1 unsigned |
| `SINT` | 8 bits signed | -128..127 |
| `INT` | 16 bits signed | -32 768..32 767 |
| `DINT` | 32 bits signed | -2³¹..2³¹-1 |
| `LINT` | 64 bits signed | -2⁶³..2⁶³-1 |
| `USINT` | 8 bits unsigned | 0..255 |
| `UINT` | 16 bits unsigned | 0..65 535 |
| `UDINT` | 32 bits unsigned | 0..2³²-1 |
| `ULINT` | 64 bits unsigned | 0..2⁶⁴-1 |
| `REAL` | 32 bits IEEE-754 | ~7 significant decimal digits |
| `LREAL` | 64 bits IEEE-754 | ~15 significant decimal digits |
| `TIME` | impl-defined | duration, e.g. `T#1h30m` |
| `DATE` | impl-defined | calendar date, e.g. `D#2026-05-14` |
| `TIME_OF_DAY` / `TOD` | impl-defined | wall-clock time, e.g. `TOD#14:30:00` |
| `DATE_AND_TIME` / `DT` | impl-defined | timestamp, `DT#2026-05-14-14:30:00` |
| `STRING` | impl-defined | variable-length character string |

## IEC reference

IEC 61131-3 third edition (2013), clause **6.4** — "Data
types".

## ForgeIEC notes

- The ForgeIEC pool stores every variable's IEC type as a
  string field. The MCP tool `project.list_pool_variables`
  returns it in the `iec_type` field of each entry.
- The ForgeIEC ST code generator emits matiec-compatible IEC
  types verbatim — no remapping. A variable declared `INT` in
  the editor is `INT` to matiec.
