---
title: "Lexical elements"
summary: "Whitespace, identifiers, comments. The character-level rules that apply to every IEC 61131-3 source file."
weight: 10
iec_chapter: "6.1"
construct_kind: "lexical"
keywords: ["identifier", "comment", "whitespace", "(*", "*)", "//", "case-insensitive"]
llm_signals:
  - error_pattern: "Unexpected token: '/'"
    where: "FStCompiler"
    diagnosis: "C/C++/Java single-line comment `// …` used. IEC 61131-3 second edition only had `(* … *)`; the third edition (2013) added `// …` but matiec's parser predates that and rejects it."
    fix_strategy: "Use the IEC `(* … *)` block-comment form for all comments."
    fix_example: |
      (* before — fails *)
      // initial step
      iCount := 0;
      (* after — IEC syntax *)
      (* initial step *)
      iCount := 0;
  - error_pattern: "Unterminated comment"
    where: "FStCompiler"
    diagnosis: "A `(*` was opened but no `*)` closes it. The parser scans to end of file looking for the closing token."
    fix_strategy: "Add the missing `*)`. Beware of nested comments — IEC ST does NOT support comment nesting; an inner `*)` closes the outer one."
    fix_example: |
      (* before — fails: nested * ) *)
      (* outer (* inner *) more outer *)
      (* after — flatten or rephrase *)
      (* outer / inner / more outer *)
  - error_pattern: "invalid identifier"
    where: "FStCompiler"
    diagnosis: "Identifier doesn't match the IEC rules: starts with a digit, contains a hyphen / dot / space, or is a reserved keyword."
    fix_strategy: "First char must be a letter or underscore; rest may be letters, digits, underscores. No hyphens, dots, spaces. No double-underscore (reserved). No reserved keyword."
    fix_example: |
      (* before — fails *)
      VAR
          1stStep : INT;            (* starts with digit *)
          step-counter : INT;       (* hyphen *)
          IF : BOOL;                (* reserved keyword *)
      END_VAR
      (* after *)
      VAR
          iFirstStep : INT;
          iStepCounter : INT;
          xIfActive : BOOL;
      END_VAR
---

## Whitespace

Spaces, tabs, line endings (CR, LF, CRLF) separate tokens.
Multiple whitespace characters are equivalent to one. ST is
**not** indentation-sensitive (unlike Python); use whatever
indentation makes the code readable.

## Identifiers

An identifier is a sequence of letters, digits and underscores
that:

- starts with a **letter or underscore** (not a digit);
- doesn't contain two **consecutive underscores** (`__` is
  reserved by the standard for implementation-internal use);
- doesn't end with an underscore (style convention; matiec
  accepts it);
- is **not a reserved keyword**.

Identifiers are **case-insensitive** per IEC 61131-3 §1.4.2.
`iCount`, `ICOUNT`, `icount` and `Icount` all refer to the
same variable. ForgeIEC normalises display to mixed-case but
accepts any spelling in source.

### Reserved keywords

The standard reserves all of:

```
ABS ACOS ACTION ADD AND ANDN ANY ANY_BIT ANY_DATE ANY_INT
ANY_NUM ANY_REAL ARRAY ASIN AT ATAN AUTHOR BCD_TO_INT
BCD_TO_DINT BCD_TO_LINT BOOL BY BYTE CAL CALC CALCN CASE
CD CONCAT CONFIGURATION CONSTANT COS CTD CTU CTUD D DATE
DATE_AND_TIME DELETE DINT DIV DO DT DWORD ELSE ELSIF
END_ACTION END_CASE END_CONFIGURATION END_FOR END_FUNCTION
END_FUNCTION_BLOCK END_IF END_PROGRAM END_REPEAT END_RESOURCE
END_STEP END_STRUCT END_TRANSITION END_TYPE END_VAR END_WHILE
EQ EXIT EXP F_EDGE F_TRIG FALSE FIND FOR FROM FUNCTION
FUNCTION_BLOCK GE GT IF IN INITIAL_STEP INSERT INT INTERVAL
JMP JMPC JMPCN LD LDN LE LEFT LEN LIMIT LINT LN LO LOG
LREAL LT LWORD MAX MID MIN MOD MUL MUX NE NOT NOW OF ON
OR ORN PRIORITY PROGRAM Q QU QD R R_EDGE R_TRIG READ_ONLY
READ_WRITE REAL REPEAT REPLACE RESOURCE RET RETC RETCN
RETAIN RETURN RIGHT ROL ROR RS S SD SDT SEL SHL SHR SIN
SINGLE SINT SR ST STN STEP STRING STRUCT SUB TAN T TASK
THEN TIME TIME_OF_DAY TO TOD TOF TON TP TRANSITION TRUE
TRUNC TYPE UDINT UINT ULINT UNTIL USINT VAR VAR_ACCESS
VAR_CONFIG VAR_EXTERNAL VAR_GLOBAL VAR_INPUT VAR_IN_OUT
VAR_OUTPUT VAR_TEMP WHILE WITH WORD WSTRING XOR
```

Plus the type-prefix forms (`BYTE#`, `INT#`, …) and the literal
prefixes (`T#`, `D#`, `TOD#`, `DT#`, `2#`, `8#`, `16#`).

### Length

The standard recommends portable code keep identifiers under
24 characters; matiec accepts up to 256. ForgeIEC's editor
shows truncation warnings if an identifier exceeds the
target-PLC's limit (settable per-project).

## Comments

Two forms accepted by IEC 61131-3 third edition:

- **Block comments**: `(* … *)` — span any number of lines,
  cannot nest.
- **Line comments**: `// …` — to end of line. **Added in the
  third edition (2013); matiec rejects them.** Use the block
  form for portability.

```iec-st
(* this is a block comment, the canonical form *)

(* multi-line block comments
   work too; the closing *)
   ends them *)

(* nesting (* doesn't work *) the inner *) closes outer *)
```

For inline notes that document a single line, write the block
form on the same line:

```iec-st
iCount := iCount + 1;        (* increment per cycle *)
```

## Pragmas

The standard does not define pragmas. ForgeIEC's editor
recognises a few non-standard pragma forms in comments
(`(*$ ForgeIEC: monitor=true *)`, etc.) for editor-specific
metadata. These pragmas survive round-trip but matiec ignores
them.

## IEC reference

IEC 61131-3 third edition (2013), clause **6.1** — "Common
elements" → "Use of printed characters".

## matiec conformance

- Whitespace: per spec.
- Identifiers: per spec, case-insensitive matching.
- Block comments: per spec.
- Line comments (`//`): NOT supported (see `llm_signals`).
- Comment nesting: not supported (per spec — both implementations
  agree).
