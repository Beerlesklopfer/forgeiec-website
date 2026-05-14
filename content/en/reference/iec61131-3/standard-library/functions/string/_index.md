---
title: "String functions"
summary: "LEN, LEFT, RIGHT, MID, CONCAT, INSERT, DELETE, REPLACE, FIND. All work on STRING; matiec also has WSTRING variants."
weight: 40
iec_chapter: "Annex F.2.5"
construct_kind: "function"
keywords: ["LEN", "LEFT", "RIGHT", "MID", "CONCAT", "INSERT", "DELETE", "REPLACE", "FIND", "STRING"]
llm_signals:
  - error_pattern: "STRING length out of range"
    where: "runtime"
    diagnosis: "An OUT-bound `STRING(N)` variable was assigned a longer value than N. matiec truncates silently."
    fix_strategy: "Either widen the target STRING(N), or `LEFT(IN := s, L := N)` the value to the target's max length first."
    fix_example: |
      VAR sShort : STRING(16); END_VAR
      sShort := LEFT(IN := sLongInput, L := 16);
  - error_pattern: "MID with L exceeds string length"
    where: "runtime"
    diagnosis: "MID with `L` longer than the substring available returns whatever is available (truncated). Not a fault but often unintended."
    fix_strategy: "Cap L with MIN against the remaining length: `MID(IN, L := MIN(L, LEN(IN) - P + 1), P := P)`."
---

## LEN — string length

`LEN(IN: STRING): INT` — number of characters in `IN`. Empty
string returns 0.

```iec-st
iN := LEN('hello');           (* → 5 *)
iN := LEN('');                (* → 0 *)
iN := LEN(sUserInput);
```

## LEFT, RIGHT, MID — substring extraction

```iec-st
sPrefix := LEFT(IN := 'forgeiec', L := 5);   (* → 'forge' *)
sSuffix := RIGHT(IN := 'forgeiec', L := 3);  (* → 'iec' *)
sMiddle := MID(IN := 'forgeiec', L := 3, P := 4);  (* → 'gei' *)
```

| Function | Signature | Notes |
|---|---|---|
| `LEFT` | `(IN: STRING, L: INT): STRING` | First `L` chars |
| `RIGHT` | `(IN: STRING, L: INT): STRING` | Last `L` chars |
| `MID` | `(IN: STRING, L: INT, P: INT): STRING` | `L` chars starting at position `P` (1-based) |

Position counting in `MID` is **1-based** per IEC convention,
not 0-based. The first character is `P := 1`.

## CONCAT — concatenation

`CONCAT(IN1: STRING, IN2: STRING, ...): STRING` — joins all
arguments end-to-end. Variadic up to ~32 args in matiec.

```iec-st
sFull := CONCAT('Hello, ', sName, '! Welcome.');
```

In ST you can also use the `+` operator on strings if the
implementation supports it; matiec accepts both `+` and
`CONCAT` for binary case but only `CONCAT` for variadic.

## INSERT — splice into a string

`INSERT(IN1: STRING, IN2: STRING, P: INT): STRING` — returns
`IN1` with `IN2` inserted after position `P`.

```iec-st
sNew := INSERT(IN1 := 'hello world',
               IN2 := 'beautiful ',
               P := 6);
(* → 'hello beautiful world' *)
```

## DELETE — remove a substring

`DELETE(IN: STRING, L: INT, P: INT): STRING` — returns `IN`
with `L` characters starting at position `P` removed.

```iec-st
sStripped := DELETE(IN := 'hello world',
                    L := 5,
                    P := 7);
(* → 'hello ' *)
```

## REPLACE — substitute a substring

`REPLACE(IN1: STRING, IN2: STRING, L: INT, P: INT): STRING` —
in `IN1`, replace `L` characters starting at position `P` with
`IN2`.

```iec-st
sFixed := REPLACE(IN1 := 'hello world',
                  IN2 := 'matiec',
                  L := 5,
                  P := 7);
(* → 'hello matiec' *)
```

## FIND — locate a substring

`FIND(IN1: STRING, IN2: STRING): INT` — returns the position
(1-based) of the first occurrence of `IN2` in `IN1`, or `0`
if `IN2` is not found.

```iec-st
iPos := FIND(IN1 := 'hello world', IN2 := 'world');  (* → 7 *)
iPos := FIND(IN1 := 'hello',       IN2 := 'xyz');    (* → 0 *)
```

## WSTRING variants

For wide-character strings (`WSTRING`, 16-bit per char),
matiec provides variants with the same names: `LEN_WSTRING`,
`LEFT_WSTRING`, etc. Use them when the source data needs to
preserve non-ASCII characters across the conversion. Most
ForgeIEC projects work in `STRING` (8-bit) and only switch to
`WSTRING` for HMI text exchange.

## IEC reference

IEC 61131-3 third edition (2013), Annex **F.2.5** —
"Character string functions" Table F.10.

## matiec conformance

All standard string functions implemented. Two practical
points:

- **1-based positions** in `MID`/`INSERT`/`DELETE`/`REPLACE`/`FIND`
  per IEC convention. Off-by-one bugs are common when porting
  from C / Python.
- **Silent truncation** when assigning a longer string to a
  shorter target. Use `LEN` + range-check up front when input
  size matters.
