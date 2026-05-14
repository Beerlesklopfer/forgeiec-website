---
title: "Common elements"
summary: "Lexical layer, data types, variable model, POU model, configuration / resources / tasks."
weight: 20
---

## Common elements

The shared foundation that all five IEC 61131-3 languages build
on. Covers everything that is independent of the per-language
syntax. (Stub — to be written.)

Sub-pages:

- [Lexical elements](lexical/) — whitespace, identifiers,
  comments, the keyword reserved list. Numeric literals live
  on the ST side at
  [textual/structured-text/literals/integer-literals/](../textual/structured-text/literals/integer-literals/).
- [Data types](data-types/) — `BOOL`, integer and bit-string
  families, `REAL` / `LREAL`, time / date types, `STRING`.
- [Generic types](generic-types/) — `ANY`, `ANY_NUM`, `ANY_INT`,
  `ANY_BIT`, `ANY_REAL`. The type-family markers used in
  standard-function signatures.
- [Derived types](derived-types/) — `STRUCT`, `ARRAY`, enums,
  type aliases, subranges. User-defined types via `TYPE …
  END_TYPE`.
- [Variable declarations](variable-declarations/) — `VAR`,
  `VAR_INPUT`, `VAR_OUTPUT`, `VAR_IN_OUT`, `VAR_TEMP`,
  `VAR_GLOBAL`, `VAR_EXTERNAL`, modifiers.
- [POU model](pou-model/) — `PROGRAM`, `FUNCTION_BLOCK`,
  `FUNCTION`: the three POU kinds and when to pick which.
- [Configuration](configuration/) — `CONFIGURATION`, `RESOURCE`,
  `TASK`, `PROGRAM`-instance binding. The IEC scheduler model.
