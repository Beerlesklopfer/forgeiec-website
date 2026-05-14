---
title: "Type-conversion functions"
summary: "Every IEC 61131-3 explicit type cast: <SRC>_TO_<DST>, TRUNC, BCD_TO_INT, INT_TO_BCD. The most-called family in matiec-strict code."
weight: 10
iec_chapter: "Annex F.2.1"
construct_kind: "function"
keywords: ["TYPE_TO_TYPE", "INT_TO_REAL", "BYTE_TO_INT", "TRUNC", "BCD"]
llm_signals:
  - error_pattern: "incompatible types in (assignment|comparison|argument)"
    where: "matiec"
    diagnosis: "matiec is strict about type matches. The fix is almost always: insert an explicit `<SRC>_TO_<DST>` call to convert one side."
    fix_strategy: "Identify the source type and the target type, then use the matching `<SRC>_TO_<DST>` function name. The names are mechanical: `INT_TO_REAL`, `BYTE_TO_INT`, `STRING_TO_INT`, etc."
    fix_example: |
      (* before — fails *)
      rResult := INT_var + REAL_var;
      (* after *)
      rResult := INT_TO_REAL(INT_var) + REAL_var;
  - error_pattern: "TRUNC.*expected REAL"
    where: "matiec"
    diagnosis: "`TRUNC` is the only IEC 61131-3 function for REAL→INT conversion (truncates toward zero). It expects a `REAL` or `LREAL` input; passing an integer is a type error."
    fix_strategy: "Use `TRUNC` only for REAL→DINT. For INT→DINT or similar integer-to-integer widening, use the regular `<SRC>_TO_<DST>` form."
    fix_example: |
      (* before — fails *)
      diOut := TRUNC(iCount);
      (* after *)
      diOut := INT_TO_DINT(iCount);
---

## The naming pattern

Every conversion is `<SRC>_TO_<DST>` where source and target
are IEC type names:

```text
<integer>_TO_<integer>     INT_TO_DINT, DINT_TO_INT, SINT_TO_LINT, ...
<integer>_TO_<unsigned>    INT_TO_UINT, DINT_TO_UDINT, ...
<unsigned>_TO_<integer>    UINT_TO_INT, UDINT_TO_DINT, ...
<integer>_TO_<bit-string>  INT_TO_BYTE, INT_TO_WORD, INT_TO_DWORD, ...
<bit-string>_TO_<integer>  BYTE_TO_INT, WORD_TO_DINT, ...
<num>_TO_REAL              INT_TO_REAL, DINT_TO_LREAL, ...
TRUNC                      REAL → DINT (truncate toward zero)
TRUNC_INT                  REAL → INT
TRUNC_LINT                 LREAL → LINT
<num>_TO_STRING            INT_TO_STRING, REAL_TO_STRING, ...
STRING_TO_<num>            STRING_TO_INT, STRING_TO_REAL, ...
<bool>_TO_<x>              BOOL_TO_INT, BOOL_TO_BYTE (TRUE → 1)
<x>_TO_BOOL                INT_TO_BOOL (0 → FALSE, anything else → TRUE)
TIME_TO_<x>                TIME_TO_DINT (returns ms), TIME_TO_REAL
<x>_TO_TIME                DINT_TO_TIME (interprets as ms)
DATE_TO_DT                 DATE → DATE_AND_TIME
DT_TO_DATE                 DATE_AND_TIME → DATE
DT_TO_TOD                  DATE_AND_TIME → TIME_OF_DAY
BCD_TO_INT                 BCD-encoded BYTE/WORD → INT/DINT
INT_TO_BCD                 INT/DINT → BCD-encoded BYTE/WORD
```

## Range and precision

Conversions that **lose information** silently truncate or
wrap. Some examples:

| Conversion | Lossy when |
|---|---|
| `DINT_TO_INT` | source out of -32 768..32 767 → wraps |
| `INT_TO_BYTE` | source out of 0..255 → wraps |
| `REAL_TO_INT` (via `TRUNC_INT`) | source out of INT range → wraps; fractional digits dropped |
| `STRING_TO_INT` | source not parseable → returns 0 (matiec); silent failure |
| `LREAL_TO_REAL` | source has more than ~7 significant digits → rounded |

For safety-critical conversions, range-check **before** the call:

```iec-st
IF dwSource >= -32768 AND dwSource <= 32767 THEN
    iTarget := DINT_TO_INT(dwSource);
ELSE
    (* handle out-of-range *)
END_IF;
```

## TRUNC vs. ROUND

IEC 61131-3 only standardises `TRUNC` (truncate toward zero).
There is no `ROUND`, `CEILING`, `FLOOR` in the standard
library. If you need rounding, do it by hand:

```iec-st
(* round to nearest INT *)
iRounded := REAL_TO_DINT(rValue + SEL(rValue < 0.0, 0.5, -0.5));

(* CEILING: round up *)
iCeiling := TRUNC_DINT(rValue + 0.999999);

(* FLOOR: round down *)
iFloor := TRUNC_DINT(rValue);
IF rValue < 0.0 AND (REAL_TO_DINT(rValue) <> rValue) THEN
    iFloor := iFloor - 1;
END_IF;
```

## BCD encoding

`BCD_TO_INT` / `INT_TO_BCD` convert between binary integer and
BCD (binary-coded decimal) packed into a `BYTE` / `WORD`.
BCD is what older 7-segment-display drivers and some legacy
PLC interfaces expose.

```iec-st
(* read packed BCD from a hardware register *)
iValue := BCD_TO_INT(bRawHardware);

(* write to a 7-segment driver *)
bDisplay := INT_TO_BCD(iValue);
```

## IEC reference

IEC 61131-3 third edition (2013), Annex F.2.1 —
"Type-conversion functions" Table F.1.

## matiec conformance

matiec implements every conversion in the table. Two practical
notes:

- **String parsing** (`STRING_TO_INT`, `STRING_TO_REAL`)
  returns `0` on parse failure rather than raising; always
  validate the source string yourself if the input is
  user-controlled.
- **No automatic widening**: an `INT` argument to a function
  expecting `DINT` requires an explicit `INT_TO_DINT` call.
  See the `llm_signals` block for the canonical fix.

## ForgeIEC notes

The editor's auto-completion suggests the matching
`<SRC>_TO_<DST>` call when it detects a type-mismatch in an
expression. The MCP `forge.help_for` tool consults this page's
`llm_signals` to translate "incompatible types" errors into
actionable conversion-call insertions.
