---
title: "Textual languages"
summary: "ST and IL — IEC 61131-3 textual programming languages."
weight: 30
---

## Textual languages

The two text-based PLC languages of IEC 61131-3:

### [Structured Text (ST)](structured-text/)

Pascal-like, statement-oriented, strongly typed. Default language
for new POUs in ForgeIEC. The deepest sub-tree in this reference
because it is the day-to-day language and carries the highest
volume of LLM-actionable diagnostics.

### [Instruction List (IL)](instruction-list/)

Assembly-like, accumulator-oriented. **Deprecated** in IEC
61131-3 third edition (2013), but matiec still accepts it and a
small number of legacy POUs in older projects use it. Documented
here for round-trip integrity. (Stub.)
