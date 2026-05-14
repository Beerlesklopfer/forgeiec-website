---
title: "Derived data types"
summary: "User-defined types: STRUCT, ARRAY, enumerations, type-safe aliases, ranges. Declared via TYPE … END_TYPE."
weight: 30
iec_chapter: "6.4.3"
construct_kind: "type"
keywords: ["TYPE", "END_TYPE", "STRUCT", "ARRAY", "enum", "alias", "range", "subrange"]
llm_signals:
  - error_pattern: "type '.*' undeclared"
    where: "matiec"
    diagnosis: "A user-defined type is referenced before it is declared. matiec processes TYPE blocks in source order; forward references inside one TYPE block work, across blocks they don't."
    fix_strategy: "Move the TYPE definition above the first reference. ForgeIEC's editor stores TYPE definitions in a dedicated POU type that the save-step orders before all using POUs."
    fix_example: |
      (* this works — STRUCT defined before use *)
      TYPE
          MY_STRUCT : STRUCT
              iCount : INT;
              xActive : BOOL;
          END_STRUCT;
      END_TYPE
      VAR myVar : MY_STRUCT; END_VAR
  - error_pattern: "ARRAY size mismatch"
    where: "matiec"
    diagnosis: "An ARRAY initialiser has fewer or more values than the declared size. matiec is strict — both ends must match."
    fix_strategy: "Either pad the initialiser with the right number of zeros / matching values, or omit the initialiser entirely (the type's default zero is used for every element)."
    fix_example: |
      (* before — fails: ARRAY[1..5] but only 3 inits *)
      arr : ARRAY[1..5] OF INT := [10, 20, 30];
      (* after — pad to match *)
      arr : ARRAY[1..5] OF INT := [10, 20, 30, 0, 0];
      (* or omit init entirely *)
      arr : ARRAY[1..5] OF INT;
---

## TYPE … END_TYPE

User-defined types live in a dedicated `TYPE` block (or in
ForgeIEC's case, in their own DataType POU):

```iec-st
TYPE
    MyStruct : STRUCT
        iCount : INT;
        xActive : BOOL;
    END_STRUCT;

    MyArray : ARRAY[1..10] OF INT;

    MyEnum : (IDLE, RUNNING, FAULTED);

    MyAlias : INT;        (* type-safe alias *)

    Percent : INT (0..100);   (* subrange *)
END_TYPE
```

After the type is declared, it can be used in any subsequent
variable declaration:

```iec-st
VAR
    state : MyStruct;
    values : MyArray;
    mode : MyEnum := IDLE;
    progress : Percent := 0;
END_VAR
```

## STRUCT — record type

Bundles named members of any types (including other STRUCTs
and ARRAYs):

```iec-st
TYPE
    SensorReading : STRUCT
        rValue : REAL;
        tTimestamp : TIME;
        xValid : BOOL;
        sUnit : STRING(8);
    END_STRUCT;
END_TYPE

VAR
    reading : SensorReading;
END_VAR

(* Access members with . *)
reading.rValue := 23.5;
reading.tTimestamp := T#0s;
reading.xValid := TRUE;

IF reading.xValid AND reading.rValue > 100.0 THEN
    DoSomething();
END_IF;
```

STRUCT members are stored contiguously in memory (with
implementation-defined alignment) and can be passed by
reference via `VAR_IN_OUT`.

## ARRAY — fixed-size collection

```iec-st
VAR
    arr : ARRAY[1..10] OF INT;                   (* 1-D *)
    matrix : ARRAY[1..3, 1..3] OF REAL;          (* 2-D *)
    cube : ARRAY[0..9, 0..9, 0..9] OF BOOL;      (* 3-D *)

    arrInit : ARRAY[1..5] OF INT := [1, 2, 3, 4, 5];   (* with init *)
    arrZero : ARRAY[1..100] OF INT;              (* zero-init *)
END_VAR

(* Access with [] *)
arr[1] := 42;
matrix[2, 3] := 1.5;
xBit := cube[5, 5, 5];
```

Bounds in the declaration are inclusive on both ends —
`ARRAY[1..10]` has ten elements with indices 1 through 10.
The lower bound doesn't have to be `0` or `1`; `ARRAY[-5..5]`
is a valid 11-element array.

Array index expressions must be `ANY_INT`. Out-of-bounds
runtime access is **implementation-defined** in matiec — may
wrap, may corrupt adjacent memory. Validate indices yourself
when they're computed at runtime.

## Enumerations

```iec-st
TYPE
    StateMachine : (IDLE, RUNNING, PAUSING, PAUSED, FAULTED);
END_TYPE

VAR
    state : StateMachine := IDLE;
END_VAR

state := RUNNING;
IF state = FAULTED THEN ... END_IF;
```

Enum literals don't need a type prefix — bare `IDLE`,
`RUNNING`, `FAULTED`. ForgeIEC's editor convention adds a
single-letter `e` prefix to the type name (`eStateMachine`)
to distinguish enum types from STRUCT types in code review;
see Memory: `feedback_enum_prefix`.

Enum values are stored as `INT`-equivalent integers, but
arithmetic on them is rejected by matiec (`state + 1` is a
type error). Use a real INT counter and convert.

## Type-safe aliases

```iec-st
TYPE
    Centimetres : INT;
    Inches : INT;
END_TYPE

VAR
    cm : Centimetres := 100;
    inch : Inches := 25;
END_VAR

(* matiec allows the assignment because both alias INT *)
cm := inch;        (* compiles, but semantically wrong *)
```

matiec's type aliases are **structural**, not nominal —
`Centimetres` and `Inches` are interchangeable with each
other and with bare `INT`. If you need true unit safety, wrap
each unit in a single-field STRUCT:

```iec-st
TYPE
    Centimetres : STRUCT iValue : INT; END_STRUCT;
    Inches : STRUCT iValue : INT; END_STRUCT;
END_TYPE
```

Now `cm := inch` is a type error.

## Subranges

```iec-st
TYPE
    Percent : INT (0..100);
    Pin : USINT (0..7);
END_TYPE
```

A subrange is `<base_type> (<min>..<max>)`. matiec **does not
range-check at runtime** — assigning `Percent := 200` compiles
and the variable holds `200`. The subrange is a documentation
hint, not a runtime guard. If you need actual range
enforcement, use `LIMIT` at every assignment site.

## IEC reference

IEC 61131-3 third edition (2013), clause **6.4.3** — "Derived
data types".

## matiec conformance

- STRUCT, ARRAY, enums implemented per the standard.
- Type aliases are structural (no nominal type-safety).
- Subranges are unchecked at runtime.
- Forward type references across separate `TYPE` blocks
  don't work — see `llm_signals`.
