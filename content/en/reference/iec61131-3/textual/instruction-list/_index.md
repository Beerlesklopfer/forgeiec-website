---
title: "Instruction List (IL)"
summary: "Accumulator-based assembly-style PLC language. Deprecated in IEC 61131-3 third edition (2013); still supported by matiec."
weight: 20
---

## Instruction List

IL is an accumulator-oriented language: every instruction reads
or writes a single implicit "current result" register and one
operand. Closer to a PLC's micro-instructions than to a
general-purpose programming language.

**Status in IEC 61131-3 third edition (2013): deprecated.**

The standard committee marked IL as obsolete because its
implicit single-accumulator model does not extend to modern
PLCs (which all run multi-task ST/FBD code on top). matiec
still accepts IL — round-trip parity for legacy PLCs and for
the small number of IL POUs in older ForgeIEC projects. New
POUs in ForgeIEC default to ST.

### Sub-pages

- [Mnemonics](mnemonics/) — full IL instruction-set
  reference: load/store, arithmetic, bitwise, comparison,
  branch, FB call, accumulator semantics, plus a step-by-step
  IL → ST migration table.
