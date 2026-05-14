---
title: "Generic data types"
summary: "ANY, ANY_NUM, ANY_INT, ANY_BIT, ANY_REAL — type-family markers used in standard-function signatures. Not usable in user variable declarations."
weight: 25
iec_chapter: "6.4.2"
construct_kind: "type"
keywords: ["ANY", "ANY_NUM", "ANY_INT", "ANY_BIT", "ANY_REAL", "ANY_DATE", "generic"]
---

## What generic types are

Generic types are **type families** — they group concrete
elementary types under one name. They appear in IEC standard-
library function signatures and let a function accept several
related types without listing each one explicitly.

```text
ABS(IN: ANY_NUM): ANY_NUM     (* ABS works on any signed numeric *)
SHL(IN: ANY_BIT, N: UINT): ANY_BIT  (* SHL works on any bit-string *)
```

**You cannot declare a variable of a generic type.**
`iCount : ANY_NUM` is a syntax error. The generic types only
exist in function-signature slots; the actual variable type
must be a concrete elementary type.

## The generic type hierarchy

```text
ANY
├── ANY_DERIVED           (* user-defined STRUCT/ARRAY/enum *)
└── ANY_ELEMENTARY
    ├── ANY_MAGNITUDE
    │   ├── ANY_NUM
    │   │   ├── ANY_REAL
    │   │   │   ├── REAL
    │   │   │   └── LREAL
    │   │   └── ANY_INT
    │   │       ├── ANY_SIGNED       (* SINT, INT, DINT, LINT *)
    │   │       └── ANY_UNSIGNED     (* USINT, UINT, UDINT, ULINT *)
    │   └── TIME
    ├── ANY_BIT
    │   ├── BOOL
    │   ├── BYTE
    │   ├── WORD
    │   ├── DWORD
    │   └── LWORD
    ├── ANY_STRING
    │   ├── STRING
    │   └── WSTRING
    └── ANY_DATE
        ├── DATE
        ├── TIME_OF_DAY
        └── DATE_AND_TIME
```

A function declared as `(IN: ANY_NUM)` accepts any of the
concrete types under `ANY_NUM` (so all `INT`, `DINT`, `REAL`,
`USINT`, etc., but **not** `BOOL` or `STRING`).

## Practical use — reading library signatures

When you call `library.read_block("ABS")` over MCP, the
returned signature is:

```text
ABS(IN: ANY_NUM): ANY_NUM
```

This means:

- Pass any concrete `ANY_NUM` value as `IN`.
- The return type is the same concrete type as `IN`. So
  `ABS(iVar)` (where iVar : INT) returns an INT;
  `ABS(rVar)` (where rVar : REAL) returns a REAL.

matiec resolves the generic at call time to the concrete type
of the argument and emits a type-specific C function call.

## Type-promotion does NOT happen automatically

Even though both `INT` and `DINT` are under `ANY_INT`, a
function declared `(IN: ANY_INT): ANY_INT` does NOT mix them
in one call. If you write:

```iec-st
result := MAX(iA, dwB);          (* INT + DINT — fails *)
```

matiec rejects the call because the two inputs disagree on
the concrete `ANY_INT` resolution. You have to convert one
side:

```iec-st
result := MAX(INT_TO_DINT(iA), dwB);
```

## IEC reference

IEC 61131-3 third edition (2013), clause **6.4.2** —
"Generic data types".

## matiec conformance

matiec implements the generic-type hierarchy as described.
The library function signatures returned by
`library.read_block` use generic-type names directly. The
no-implicit-promotion rule is the recurring porting pain
point — see the [type-conversion functions](../../standard-library/functions/type-conversion/)
page for the explicit `<SRC>_TO_<DST>` fixes.
