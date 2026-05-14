---
title: "Bitwise & logical operators"
summary: "AND, OR, XOR, NOT — same keywords for bitwise and logical operations; the operand type decides which."
weight: 20
iec_chapter: "6.6.1"
construct_kind: "operator"
keywords: ["AND", "OR", "XOR", "NOT", "&", "bitwise", "logical"]
llm_signals:
  - error_pattern: "AND of BOOL and BYTE"
    where: "matiec"
    diagnosis: "An AND/OR/XOR is mixing a `BOOL` operand with a `BYTE`/`WORD`/`DWORD` operand. matiec does not auto-extract a single bit from a multi-bit type to do a logical AND."
    fix_strategy: "Extract the bit explicitly with bit-access syntax `bMask.0`, or convert the BOOL into a single-bit BYTE, or convert the BYTE into a BOOL via `<> 0`."
    fix_example: |
      (* before — fails *)
      IF xEnable AND bMask THEN ... END_IF;
      (* after — option A: extract bit *)
      IF xEnable AND bMask.0 THEN ... END_IF;
      (* after — option B: convert BYTE to BOOL *)
      IF xEnable AND (bMask <> 0) THEN ... END_IF;
  - error_pattern: "SHL was not declared in this scope"
    where: "gcc"
    diagnosis: "matiec emit-bug — `SHL(BYTE#1, INT_TO_UINT(x))` produces broken C-code that gcc rejects. The `SHL` symbol is not in the matiec runtime header in this combination."
    fix_strategy: "Replace the bit-shift with an `IF/ELSIF` cascade or `CASE OF` over decimal literals (1, 2, 4, 8, 16, 32, …). Documented in detail at [literals/integer-literals](../../literals/integer-literals/) and [control-flow/case-statement](../../control-flow/case-statement/)."
    fix_example: |
      (* before — fails on PLC g++ *)
      bMask := SHL(BYTE#1, INT_TO_UINT(iStep));
      (* after — explicit dispatch *)
      IF iStep = 0 THEN bMask := INT_TO_BYTE(1);
      ELSIF iStep = 1 THEN bMask := INT_TO_BYTE(2);
      ELSIF iStep = 2 THEN bMask := INT_TO_BYTE(4);
      (* ... *)
      END_IF;
---

## The same operators do two jobs

`AND`, `OR`, `XOR`, `NOT` work on:

- **`BOOL`** — logical operations. `xA AND xB` is the logical
  AND of two booleans.
- **`BYTE`/`WORD`/`DWORD`/`LWORD`** — bitwise operations.
  `bA AND bB` is the bitwise AND of every bit-pair.

The operand type decides which. **Mixing `BOOL` and a multi-
bit type in one operation is illegal** (matiec rejects it).

`&` is a synonym for `AND` (both equally valid). The IEC
standard prefers `AND`; some older code uses `&`.

## Operators

| Op | Meaning | BOOL operands | Bit-string operands |
|---|---|---|---|
| `NOT` | Negation | `NOT xA` flips the bool | `NOT bA` flips every bit |
| `AND`, `&` | Conjunction | logical AND | bitwise AND |
| `OR` | Disjunction | logical OR | bitwise OR |
| `XOR` | Exclusive OR | logical XOR | bitwise XOR |

There are **no shift operators** in the operator set —
`SHL`/`SHR`/`ROL`/`ROR` are functions, called like `SHL(IN, N)`.
See the [Standard Library bit functions](../../../../../standard-library/) page
(stub) and the matiec emit-bug warning in `llm_signals` above.

## Examples

```iec-st
(* logical *)
xReady := xEnable AND NOT xFault;
xAny   := xA OR xB OR xC;

(* bitwise *)
bMask  := bByte AND 16#0F;       (* keep low nibble *)
bToggle := bByte XOR 16#80;      (* flip top bit *)

(* bit-access — read one bit out of a multi-bit type as BOOL *)
xLowBit := bByte.0;
bSet    := bByte.7;

(* construct a multi-bit value from individual bools *)
(* IEC has no first-class "bool to bit" — use SEL: *)
bByte := SEL(xA, BYTE#0, BYTE#1)
       OR SEL(xB, BYTE#0, BYTE#2)
       OR SEL(xC, BYTE#0, BYTE#4);
```

## Bit-access syntax

For any `BYTE`/`WORD`/`DWORD`/`LWORD` variable named `bx`,
the expression `bx.N` accesses bit `N` (0 = least-significant)
as a `BOOL`. This works for both reads and writes:

```iec-st
xFlag := bMask.3;     (* read bit 3 of bMask as BOOL *)
bMask.5 := TRUE;      (* set bit 5 of bMask *)
```

Bit-access only works on bit-string types, not on integer types
like `INT`. If the variable is an integer, convert first
(`INT_TO_WORD`).

## Short-circuit evaluation

The IEC standard does **not** mandate short-circuit evaluation
for `AND` / `OR`. Both operands can be evaluated even when the
first one already determines the result. Don't rely on
`xPtrValid AND xPtr.SomeField` to skip the field-access when
`xPtrValid` is `FALSE` — that is an unsafe idiom in IEC ST.

In practice matiec does evaluate left-to-right and stops on
the first definitive value, but this is not portable to other
IEC compilers.

## IEC reference

IEC 61131-3 third edition (2013), clause **6.6.1** Table 55.

## matiec conformance

matiec implements `AND` / `OR` / `XOR` / `NOT` per the standard
for both BOOL and bit-string operands. The well-known emit-bug
with `SHL(BYTE#1, …)` is an emit-bug **on shift functions**,
not on the bitwise operators themselves — the operators work
correctly. See the second `llm_signals` entry above for the
workaround.
